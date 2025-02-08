import signal
import subprocess
import sys
import time
from subprocess import Popen

import keyboard
import psutil
from PIL import Image, ImageDraw
from pystray import Icon, Menu, MenuItem
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from GameSentenceMiner import anki
from GameSentenceMiner import config_gui
from GameSentenceMiner import configuration
from GameSentenceMiner import ffmpeg
from GameSentenceMiner import gametext
from GameSentenceMiner import notification
from GameSentenceMiner import obs
from GameSentenceMiner import util
from GameSentenceMiner.downloader.download_tools import download_obs_if_needed, download_ffmpeg_if_needed
from GameSentenceMiner.vad import vosk_helper, silero_trim, whisper_helper
from GameSentenceMiner.configuration import *
from GameSentenceMiner.ffmpeg import get_audio_and_trim
from GameSentenceMiner.gametext import get_line_timing
from GameSentenceMiner.util import *

if is_windows():
    import win32api

obs_process: Popen
procs_to_close = []
settings_window: config_gui.ConfigApp = None
obs_paused = False
icon: Icon
menu: Menu


class VideoToAudioHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory or ("Replay" not in event.src_path and "GSM" not in event.src_path):
            return
        if event.src_path.endswith(".mkv") or event.src_path.endswith(".mp4"):  # Adjust based on your OBS output format
            logger.info(f"MKV {event.src_path} FOUND, RUNNING LOGIC")
            time.sleep(.5)  # Small Sleep to allow for replay to be fully written
            self.convert_to_audio(event.src_path)

    @staticmethod
    def convert_to_audio(video_path):
        try:
            with util.lock:
                if os.path.exists(video_path) and os.access(video_path, os.R_OK):
                    logger.debug(f"Video found and is readable: {video_path}")

                if get_config().obs.minimum_replay_size and not ffmpeg.is_video_big_enough(video_path,
                                                                                           get_config().obs.minimum_replay_size):
                    logger.debug("Checking if video is big enough")
                    notification.send_check_obs_notification(reason="Video may be empty, check scene in OBS.")
                    logger.error(
                        f"Video was unusually small, potentially empty! Check OBS for Correct Scene Settings! Path: {video_path}")
                    return
                util.use_previous_audio = True
                last_note = None
                logger.debug("Attempting to get last anki card")
                if get_config().anki.update_anki:
                    last_note = anki.get_last_anki_card()
                if get_config().features.backfill_audio:
                    last_note = anki.get_cards_by_sentence(gametext.previous_line)
                line_time, next_line_time = get_line_timing(last_note)
                ss_timing = 0
                if line_time and next_line_time:
                    ss_timing = ffmpeg.get_screenshot_time(video_path, line_time)
                if last_note:
                    logger.debug(json.dumps(last_note))

                note = anki.get_initial_card_info(last_note)

                tango = last_note['fields'][get_config().anki.word_field]['value'] if last_note else ''

                if get_config().anki.sentence_audio_field:
                    logger.debug("Attempting to get audio from video")
                    final_audio_output, should_update_audio, vad_trimmed_audio = VideoToAudioHandler.get_audio(
                        line_time,
                        next_line_time,
                        video_path)
                else:
                    final_audio_output = ""
                    should_update_audio = False
                    vad_trimmed_audio = ""
                    logger.info("No SentenceAudio Field in config, skipping audio processing!")
                try:
                    # Only update sentenceaudio if it's not present. Want to avoid accidentally overwriting sentence audio
                    try:
                        if get_config().anki.update_anki and last_note:
                            anki.update_anki_card(last_note, note, audio_path=final_audio_output, video_path=video_path,
                                                  tango=tango,
                                                  should_update_audio=should_update_audio,
                                                  ss_time=ss_timing)
                        elif get_config().features.notify_on_update and should_update_audio:
                            notification.send_audio_generated_notification(vad_trimmed_audio)
                    except Exception as e:
                        logger.error(f"Card failed to update! Maybe it was removed? {e}")
                except FileNotFoundError as f:
                    logger.error("Something went wrong with processing, anki card not updated")
        except Exception as e:
            logger.error(f"Some error was hit catching to allow further work to be done: {e}", exc_info=1)
        if get_config().paths.remove_video and os.path.exists(video_path):
            os.remove(video_path)  # Optionally remove the video after conversion
        if get_config().paths.remove_audio and os.path.exists(vad_trimmed_audio):
            os.remove(vad_trimmed_audio)  # Optionally remove the screenshot after conversion

    @staticmethod
    def get_audio(line_time, next_line_time, video_path):
        trimmed_audio = get_audio_and_trim(video_path, line_time, next_line_time)
        vad_trimmed_audio = make_unique_file_name(
            f"{os.path.abspath(configuration.get_temporary_directory())}/{obs.get_current_game(sanitize=True)}.{get_config().audio.extension}")
        final_audio_output = make_unique_file_name(os.path.join(get_config().paths.audio_destination, f"{obs.get_current_game(sanitize=True)}.{get_config().audio.extension}"))
        should_update_audio = True
        if get_config().vad.do_vad_postprocessing:
            match get_config().vad.selected_vad_model:
                case configuration.SILERO:
                    should_update_audio = silero_trim.process_audio_with_silero(trimmed_audio, vad_trimmed_audio)
                case configuration.VOSK:
                    should_update_audio = vosk_helper.process_audio_with_vosk(trimmed_audio, vad_trimmed_audio)
                case configuration.WHISPER:
                    should_update_audio = whisper_helper.process_audio_with_whisper(trimmed_audio,
                                                                                    vad_trimmed_audio)
            if not should_update_audio:
                match get_config().vad.backup_vad_model:
                    case configuration.OFF:
                        pass
                    case configuration.SILERO:
                        should_update_audio  = silero_trim.process_audio_with_silero(trimmed_audio,
                                                                                     vad_trimmed_audio)
                    case configuration.VOSK:
                        should_update_audio  = vosk_helper.process_audio_with_vosk(trimmed_audio, vad_trimmed_audio)
                    case configuration.WHISPER:
                        should_update_audio  = whisper_helper.process_audio_with_whisper(trimmed_audio,
                                                                                         vad_trimmed_audio)
        if get_config().audio.ffmpeg_reencode_options and os.path.exists(vad_trimmed_audio):
            ffmpeg.reencode_file_with_user_config(vad_trimmed_audio, final_audio_output,
                                                  get_config().audio.ffmpeg_reencode_options)
        elif os.path.exists(vad_trimmed_audio):
            os.replace(vad_trimmed_audio, final_audio_output)
        return final_audio_output, should_update_audio, vad_trimmed_audio


def initialize(reloading=False):
    global obs_process
    if not reloading:
        if is_windows():
            download_obs_if_needed()
            download_ffmpeg_if_needed()
        if get_config().obs.enabled:
            obs_process = obs.start_obs()
            obs.connect_to_obs(start_replay=True)
            anki.start_monitoring_anki()
        gametext.start_text_monitor()
        os.makedirs(get_config().paths.folder_to_watch, exist_ok=True)
        os.makedirs(get_config().paths.screenshot_destination, exist_ok=True)
        os.makedirs(get_config().paths.audio_destination, exist_ok=True)
    if get_config().vad.do_vad_postprocessing:
        if VOSK in (get_config().vad.backup_vad_model, get_config().vad.selected_vad_model):
            vosk_helper.get_vosk_model()
        if WHISPER in (get_config().vad.backup_vad_model, get_config().vad.selected_vad_model):
            whisper_helper.initialize_whisper_model()

def initial_checks():
    try:
        subprocess.run(ffmpeg.ffmpeg_base_command_list)
        logger.debug("FFMPEG is installed and accessible.")
    except FileNotFoundError:
        logger.error("FFmpeg not found, please install it and add it to your PATH.")
        raise


def register_hotkeys():
    keyboard.add_hotkey(get_config().hotkeys.reset_line, gametext.reset_line_hotkey_pressed)
    keyboard.add_hotkey(get_config().hotkeys.take_screenshot, get_screenshot)


def get_screenshot():
    try:
        image = obs.get_screenshot()
        time.sleep(2)  # Wait for ss to save
        if not image:
            raise Exception("Failed to get Screenshot from OBS")
        encoded_image = ffmpeg.process_image(image)
        if get_config().anki.update_anki and get_config().screenshot.screenshot_hotkey_updates_anki:
            last_note = anki.get_last_anki_card()
            if last_note:
                logger.debug(json.dumps(last_note))
            if get_config().features.backfill_audio:
                last_note = anki.get_cards_by_sentence(gametext.previous_line)
            if last_note:
                anki.add_image_to_card(last_note, encoded_image)
                notification.send_screenshot_updated(last_note['fields'][get_config().anki.word_field]['value'])
                if get_config().features.open_anki_edit:
                    notification.open_anki_card(last_note['noteId'])
            else:
                notification.send_screenshot_saved(encoded_image)
        else:
            notification.send_screenshot_saved(encoded_image)
    except Exception as e:
        logger.error(f"Failed to get Screenshot {e}")


def create_image():
    """Create a simple pickaxe icon."""
    width, height = 64, 64
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))  # Transparent background
    draw = ImageDraw.Draw(image)

    # Handle (rectangle)
    handle_color = (139, 69, 19)  # Brown color
    draw.rectangle([(30, 15), (34, 50)], fill=handle_color)

    # Blade (triangle-like shape)
    blade_color = (192, 192, 192)  # Silver color
    draw.polygon([(15, 15), (49, 15), (32, 5)], fill=blade_color)

    return image


def open_settings():
    obs.update_current_game()
    settings_window.show()


def open_log():
    """Function to handle opening log."""
    """Open log file with the default application."""
    log_file_path = get_log_path()
    if not os.path.exists(log_file_path):
        logger.error("Log file not found!")
        return

    if sys.platform.startswith("win"):  # Windows
        os.startfile(log_file_path)
    elif sys.platform.startswith("darwin"):  # macOS
        subprocess.call(["open", log_file_path])
    elif sys.platform.startswith("linux"):  # Linux
        subprocess.call(["xdg-open", log_file_path])
    else:
        logger.error("Unsupported platform!")
    logger.info("Log opened.")


def exit_program(icon, item):
    """Exit the application."""
    logger.info("Exiting...")
    icon.stop()
    cleanup()


def play_pause(icon, item):
    global obs_paused, menu
    obs.toggle_replay_buffer()
    update_icon()


def update_icon():
    global menu, icon
    # Recreate the menu with the updated button text
    profile_menu = Menu(
        *[MenuItem(("Active: " if profile == get_master_config().current_profile else "") + profile, switch_profile) for profile in
          get_master_config().get_all_profile_names()]
    )

    menu = Menu(
        MenuItem("Open Settings", open_settings),
        MenuItem("Open Log", open_log),
        MenuItem("Toggle Replay Buffer", play_pause),
        MenuItem("Restart OBS", restart_obs),
        MenuItem("Switch Profile", profile_menu),
        MenuItem("Exit", exit_program)
    )

    icon.menu = menu
    icon.update_menu()

def switch_profile(icon, item):
    if "Active:" in item.text:
        logger.error("You cannot switch to the currently active profile!")
        return
    logger.info(f"Switching to profile: {item.text}")
    get_master_config().current_profile = item.text
    switch_profile_and_save(item.text)
    settings_window.reload_settings()
    update_icon()


def run_tray():
    global menu, icon

    profile_menu = Menu(
        *[MenuItem(("Active: " if profile == get_master_config().current_profile else "") + profile, switch_profile) for
          profile in
          get_master_config().get_all_profile_names()]
    )

    menu = Menu(
        MenuItem("Open Settings", open_settings),
        MenuItem("Open Log", open_log),
        MenuItem("Toggle Replay Buffer", play_pause),
        MenuItem("Restart OBS", restart_obs),
        MenuItem("Switch Profile", profile_menu),
        MenuItem("Exit", exit_program)
    )

    icon = Icon("TrayApp", create_image(), "Game Sentence Miner", menu)
    icon.run()

def close_obs():
    if obs_process:
        logger.info("Closing OBS")
        obs_process.terminate()
        obs_process.wait()

def restart_obs():
    global obs_process
    close_obs()
    time.sleep(2)
    obs_process = obs.start_obs()
    obs.connect_to_obs(start_replay=True)

def cleanup():
    logger.info("Performing cleanup...")
    util.keep_running = False

    if get_config().obs.enabled:
        if get_config().obs.start_buffer:
            obs.stop_replay_buffer()
    obs.disconnect_from_obs()
    close_obs()

    proc: Popen
    for proc in procs_to_close:
        try:
            logger.info(f"Terminating process {proc.args[0]}")
            proc.terminate()
            proc.wait()  # Wait for OBS to fully close
            logger.info(f"Process {proc.args[0]} terminated.")
        except psutil.NoSuchProcess:
            logger.info("PID already closed.")
        except Exception as e:
            proc.kill()
            logger.error(f"Error terminating process {proc}: {e}")


    settings_window.window.destroy()
    logger.info("Cleanup complete.")


def handle_exit():
    """Signal handler for graceful termination."""

    def _handle_exit(signum):
        logger.info(f"Received signal {signum}. Exiting gracefully...")
        cleanup()
        sys.exit(0)

    return _handle_exit


def main(reloading=False, do_config_input=True):
    global settings_window
    logger.info("Script started.")
    initialize(reloading)
    initial_checks()
    event_handler = VideoToAudioHandler()
    observer = Observer()
    observer.schedule(event_handler, get_config().paths.folder_to_watch, recursive=False)
    observer.start()

    logger.info("Script Initialized. Happy Mining!")
    if not is_linux():
        register_hotkeys()

    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGTERM, handle_exit())  # Handle `kill` commands
    signal.signal(signal.SIGINT, handle_exit())  # Handle Ctrl+C
    if is_windows():
        win32api.SetConsoleCtrlHandler(handle_exit())

    util.run_new_thread(run_tray)

    try:
        settings_window = config_gui.ConfigApp()
        if get_config().general.check_for_update_on_startup:
            settings_window.window.after(0, settings_window.check_update)
        if get_config().general.open_config_on_startup:
            settings_window.window.after(0, settings_window.show)
        settings_window.add_save_hook(update_icon)
        settings_window.window.mainloop()
    except KeyboardInterrupt:
        cleanup()

    try:
        observer.stop()
        observer.join()
    except Exception as e:
        logger.error(f"Error stopping observer: {e}")


if __name__ == "__main__":
    main()
