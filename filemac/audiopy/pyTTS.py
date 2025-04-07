import json
import math
import os
import PyPDF2
import shutil
import sys
from docx import Document
from threading import Lock, Thread
from typing import List, Union
import logging
import logging.handlers
import requests
from gtts import gTTS
from pydub import AudioSegment
from rich.errors import MarkupError
from ..pydocs import DocConverter
from utils.colors import foreground

logging.basicConfig(level=logging.INFO, format="%(levelname)-8s %(message)s")
logger = logging.getLogger(__name__)

fcl = foreground()
RESET = fcl.RESET

_ext_word = ["doc", "docx"]


class FileSynthesis:
    """Definition of audiofying class"""

    def __init__(
        self,
        obj: Union[os.PathLike, str, List[Union[os.PathLike, str]]],
        resume: bool = True,
    ):
        self.obj = obj
        self.resume = resume

    @staticmethod
    def join_audios(files, output_file):
        masterfile = output_file + "_master.mp3"
        print(
            f"{fcl.BBLUE_FG}Create a master file {fcl.BMAGENTA_FG}{masterfile}{RESET}",
            end="\r",
        )
        # Create a list to store files
        ogg_files = []
        # loop through the directory while adding the ogg files to the list
        for filename in files:
            print(f"Join {fcl.BBLUE_FG}{len(files)}{RESET} files")
            # if filename.endswith('.ogg'):
            # ogg_file = os.path.join(path, filename)
            ogg_files.append(AudioSegment.from_file(filename))

        # Concatenate the ogg files
        combined_ogg = ogg_files[0]
        for i in range(1, len(files)):
            combined_ogg += ogg_files[i]

        # Export the combined ogg to new mp3 file or ogg file
        combined_ogg.export(output_file + "_master.ogg", format="ogg")
        print(
            f"{fcl.BGREEN_FG}Master file:Ok                                                                             {RESET}"
        )

    def Synthesise(
        self,
        text: str,
        output_file: str,
        CHUNK_SIZE: int = 1_000,
        _tmp_folder_: str = "tmp_dir",
        thread_name: str = None,
        max_retries: int = 30,
    ) -> None:
        """Converts given text to speech using Google Text-to-Speech API."""
        # from rich.progress import (BarColumn, Progress, SpinnerColumn,TextColumn)

        config = ConfigManager()
        # Define directories and other useful variables for genrating output_file and checkpoint_file
        out_dir = os.path.split(output_file)[0]

        thread_name = f"thread_{os.path.split(output_file.split('.')[0])[-1]}"
        _file_ = os.path.split(output_file)[1]

        _tmp_folder_ = os.path.join(out_dir, _tmp_folder_)

        # Remove temporary dir if it exists, rare-cases since file names are mostly unique
        if os.path.exists(_tmp_folder_) and self.resume is False:
            # query = input(f"{fcl.BBLUE_FG}Remove the {os.path.join(out_dir, _tmp_folder_)} directory (y/n)?{RESET} ").lower() in ('y', 'yes')
            shutil.rmtree(_tmp_folder_)

        # Create temporary folder to house chunks
        if not os.path.exists(_tmp_folder_):
            logger.info(
                f"{fcl.BYELLOW_FG}Create temporary directory = {fcl.BBLUE_FG}{_tmp_folder_}{RESET}"
            )
            os.mkdir(_tmp_folder_)

        _full_output_path_ = os.path.join(_tmp_folder_, _file_)

        # Read reume chunk from the configuration file
        start_chunk = int(config.read_config_file(thread_name)) * 1_000
        start_chunk = 0 if start_chunk is None else start_chunk

        """ If chunk is not 0 multiply the chunk by the highest decimal value of the chunk size
        else set it to 0 meaning file is being operated on for the first time
        """
        resume_chunk_pos = start_chunk * 1_000 if start_chunk != 0 else start_chunk

        try:
            print(f"{fcl.BYELLOW_FG}Start thread:: {thread_name}{RESET}")

            total_chunks = math.ceil(len(text) / CHUNK_SIZE)

            counter = (
                math.ceil(resume_chunk_pos / CHUNK_SIZE) if resume_chunk_pos != 0 else 0
            )

            attempt = 0

            while attempt <= max_retries:
                try:
                    # Initialize progress bar for the overall process

                    for i in range(resume_chunk_pos, len(text), CHUNK_SIZE):
                        print(
                            f"Processing: chunk {fcl.BMAGENTA_FG}{counter}/{total_chunks} {fcl.DCYAN_FG}{counter/total_chunks*100:.2f}%{RESET}\n",
                            end="\r",
                        )
                        chunk = text[i : i + CHUNK_SIZE]
                        # print(chunk)
                        if os.path.exists(f"{_full_output_path_}_{counter}.ogg"):
                            if counter == start_chunk:
                                print(
                                    f"{fcl.CYAN_FG}Chunk vs file confict: {fcl.BLUE_FG}Resolving{RESET}"
                                )
                                os.remove(f"{_full_output_path_}_{
                                    counter}.ogg")
                                output_filename = f"{
                                    _full_output_path_}_{counter}.ogg"

                            # Remove empty file
                            elif (
                                os.path.getsize(f"{_full_output_path_}_{counter}.ogg")
                                != 0
                            ):
                                os.remove(f"{_full_output_path_}_{
                                    counter}.ogg")
                                output_filename = f"{
                                    _full_output_path_}_{counter}.ogg"

                            else:
                                output_filename = f"{
                                    _full_output_path_}_{counter+1}.ogg"

                        else:
                            output_filename = f"{
                                _full_output_path_}_{counter}.ogg"

                        tts = gTTS(text=chunk, lang="en", slow=False)

                        tts.save(output_filename)

                        # Update current_chunk in the configuration
                        config.update_config_entry(thread_name, current_chunk=counter)

                        counter += 1

                except FileNotFoundError as e:
                    logger.error(f"{fcl.RED_FG}{e}{RESET}")

                except (
                    requests.exceptions.ConnectionError
                ):  # Handle connectivity/network error
                    logger.error(f"{fcl.RED_FG}ConnectionError{RESET}")

                    # Exponential backoff for retries
                    for _sec_ in range(2**attempt, 0, -1):
                        print(
                            # Increament the attempts
                            f"{fcl.BWHITE_FG}Resume in {fcl.BBLUE_FG}{_sec_}{RESET}",
                            end="\r",
                        )

                    attempt += 1

                    # Read chunk from configuration
                    resume_chunk_pos = int(config.read_config_file(thread_name)) * 1_000

                except (
                    requests.exceptions.HTTPError
                ) as e:  # Exponential backoff for retries
                    logger.error(f"HTTP error: {e.status_code} - {e.reason}")
                    for _sec_ in range(2**attempt, 0, -1):
                        print(
                            f"{fcl.BWHITE_FG}Resume in {fcl.BBLUE_FG}{_sec_}{RESET}",
                            end="\r",
                        )

                    attempt += 1

                    resume_chunk_pos = int(config.read_config_file(thread_name)) * 1_000

                except requests.exceptions.RequestException as e:
                    logger.error(f"{fcl.RED_FG}{e}{RESET}")

                    for _sec_ in range(2**attempt, 0, -1):
                        print(
                            f"{fcl.BWHITE_FG}Resume in {fcl.BBLUE_FG}{_sec_}{RESET}",
                            end="\r",
                        )
                    attempt += 1

                    resume_chunk_pos = int(config.read_config_file(thread_name)) * 1_000

                except (
                    ConnectionError,
                    ConnectionAbortedError,
                    ConnectionRefusedError,
                    ConnectionResetError,
                ):
                    logger.error(f"{fcl.RED_FG}Connection at attempt{RESET}")

                    for _sec_ in range(2**attempt, 0, -1):
                        print(
                            f"{fcl.BWHITE_FG}Resume in {fcl.BLUE_FG}{_sec_}{RESET}",
                            end="\r",
                        )

                        attempt += 1

                    resume_chunk_pos = int(config.read_config_file(thread_name)) * 1_000

                except MarkupError as e:
                    logger.error(f"{fcl.RED_FG}{e}{RESET}")
                except Exception as e:  # Handle all other types of exceptions
                    logger.error(
                        f"{fcl.BMAGENTA_FG}{attempt+1}/{max_retries}:{fcl.RED_FG}{e}{RESET}"
                    )

                    for _sec_ in range(2**attempt, 0, -1):
                        pass

                    attempt += 1

                    resume_chunk_pos = int(config.read_config_file(thread_name)) * 1_000

                else:
                    print(
                        f"{fcl.BMAGENTA_FG}Conversion success✅. \n  {fcl.CYAN_FG}INFO\t Create masterfile{RESET}"
                    )

                    if (
                        len(os.listdir(_tmp_folder_)) > 2
                    ):  # Combine generated gTTS objects
                        from .JoinAudios import JoinAudios

                        joiner = JoinAudios(_tmp_folder_, masterfile=output_file)
                        joiner.worker()
                        # Remove temporary files
                        shutil.rmtree(_tmp_folder_)

                    break  # Exit the retry loop if successfull

            else:
                print(
                    f"{fcl.RED_FG}Maximum retries reached. Unable to complete the operation after {fcl.BMAGENTA_FG} {max_retries} attempts.{RESET}"
                )
                sys.exit(2)

        finally:
            pass

    @staticmethod
    def pdf_to_text(pdf_path):
        logger.info(f"{fcl.GREEN_FG} Initializing pdf to text conversion{RESET}")
        try:
            with open(pdf_path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                _pg_ = 0
                print(f"{fcl.YELLOW_FG}Convert pages..{RESET}")
                for page_num in range(len(pdf_reader.pages)):
                    _pg_ += 1
                    logger.info(
                        f"Page {fcl.BBLUE_FG}{_pg_}{RESET}/{len(pdf_reader.pages)}"
                    )
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
                print(f"{fcl.BGREEN_FG}Ok{RESET}\n")
                return text
        except Exception as e:
            logger.error(
                f"{fcl.RED_FG}Failed to extract text from '{fcl.YELLOW_FG}{pdf_path}'{RESET}:\n {e}"
            )

    @staticmethod
    def text_file(input_file):
        try:
            with open(input_file, "r", errors="ignore") as file:
                text = file.read().replace("\n", " ")
            return text
        except FileNotFoundError:
            logger.error("File '{}' was not found.📁".format(input_file))
        except Exception as e:
            logger.error(f"{fcl.RED_FG}{str(e)}{RESET}")

    @staticmethod
    def docx_to_text(docx_path):
        try:
            logger.info(f"{fcl.BLUE_FG} Converting {docx_path} to text{RESET}")
            doc = Document(docx_path)
            paragraphs = [paragraph.text for paragraph in doc.paragraphs]
            return "\n".join(paragraphs)
        except FileNotFoundError:
            logger.error(f"File '{docx_path}' was not found.📁")
        except Exception as e:
            logger.error(
                f"{fcl.RED_FG}Error converting {docx_path} to text: {e}\
{RESET}"
            )

    class THAudio:
        def __init__(self, instance):
            self.instance = instance
            self.lock = Lock()
            self.config = ConfigManager()

        def audiofy(self, num_threads=3):
            ls = ("pdf", "docx", "doc", "txt", "ppt", "pptx")

            def create_thread(item, thread_name):
                # Create a unique temp dir for each file
                temp_dir = f"tmp_dir_{os.path.split(item.split('.')[0])[-1]}"

                # Ensure proper locking when adding config entry
                with self.lock:
                    # Record config entry for each item
                    self.config.add_config_entry(
                        thread_name, f"{item.split('.')[0]}", temp_dir, 0
                    )

                # Create and return the thread
                return Thread(
                    target=self.worker,
                    args=(item, temp_dir, thread_name),
                    name=thread_name,
                )

            threads = []
            processed_items = 0

            # Process a list of files
            def process_batch():
                for thread in threads:
                    thread.start()
                for thread in threads:
                    thread.join()
                threads.clear()  # Clear thread list after batch is done

            # Handle files provided as a list
            if isinstance(self.instance.obj, list):
                for item in self.instance.obj:
                    item = os.path.abspath(item)
                    if os.path.isfile(item) and item.endswith(ls):
                        thread_name = f"thread_{os.path.split(item.split('.')[0])[-1]}"
                        thread = create_thread(item, thread_name)
                        threads.append(thread)
                        processed_items += 1

                        # Process threads in batches of 'num_threads'
                        if processed_items % num_threads == 0:
                            process_batch()

                # Process remaining threads in case the list isn't a perfect multiple of num_threads
                if threads:
                    process_batch()

            # Handle a single file
            elif os.path.isfile(self.instance.obj):
                item = os.path.abspath(self.instance.obj)
                if item.endswith(ls):
                    thread_name = f"thread_{os.path.split(item.split('.')[0])[-1]}"
                    thread = create_thread(item, thread_name)
                    threads.append(thread)
                    process_batch()  # Process immediately for single file

            # Handle a directory of files
            elif os.path.isdir(self.instance.obj):
                for item in os.listdir(self.instance.obj):
                    item = os.path.abspath(item)
                    if os.path.isfile(item) and item.endswith(ls):
                        thread_name = f"thread_{os.path.split(item.split('.')[0])[-1]}"
                        thread = create_thread(item, thread_name)
                        threads.append(thread)
                        processed_items += 1

                        # Process threads in batches
                        if processed_items % num_threads == 0:
                            process_batch()

                # Process remaining threads
                if threads:
                    process_batch()

        def worker(self, input_file, _temp_dir_, thread_name):
            output_file = os.path.split(input_file)[-1].split(".")[0] + ".ogg"
            print(f"Thread {thread_name} processing file: {input_file}")

            try:
                # Extract text based on file type
                if input_file.endswith(".pdf"):
                    text = FileSynthesis.pdf_to_text(input_file)
                elif input_file.lower().endswith(tuple(_ext_word)):
                    text = FileSynthesis.docx_to_text(input_file)
                elif input_file.endswith(".txt"):
                    text = FileSynthesis.text_file(input_file)
                elif input_file.split(".")[-1] in ("ppt", "pptx"):
                    conv = DocConverter(input_file)
                    word = conv.ppt_to_word()
                    conv = DocConverter(word)
                    text = FileSynthesis.text_file(conv.word_to_txt())
                else:
                    raise ValueError(
                        "Unsupported file format. Please provide a PDF, txt, or Word document."
                    )

                # Synthesize audio using the extracted text
                self.instance.Synthesise(
                    text, output_file, _tmp_folder_=_temp_dir_, thread_name=thread_name
                )
                print(f"Thread {thread_name} completed processing {input_file}")

            except Exception as e:
                print(f"Error in thread {thread_name}: {e}")
            except KeyboardInterrupt:
                print(f"Thread {thread_name} interrupted.")
                sys.exit(1)


class ConfigManager:
    def __init__(self, config_path="filemac_config.json"):
        self.config_path = config_path

    def create_config_file(self, config_data):
        """
        Create or overwrite a configuration file to record thread names, associated file names, and current chunks.

        Args:
            config_data(list): A list of dictionaries containing thread name, associated file name, temp dir, and current chunk.
        """
        try:
            # Ensure the output directory exists
            output_dir = os.path.dirname(self.config_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Write the configuration data to a JSON file
            with open(self.config_path, "w") as config_file:
                json.dump(config_data, config_file, indent=4)

            print(f"Configuration file '{self.config_path}' created successfully.")
        except Exception as e:
            print(f"Error creating configuration file: {e}")

    def read_config_file(self, thread=None):
        """
        Read the configuration file and return the data or a specific thread's current chunk.

        Args:
            thread (str): The thread name to search for in the config. If None, returns the full config.

        Returns:
            dict/list: Returns a specific entry for the thread or the full configuration data.
            None: If the file doesn't exist or thread is not found.
        """
        try:
            if not os.path.exists(self.config_path):
                print(f"Configuration file '{self.config_path}' not found.")
                return None

            with open(self.config_path, "r") as config_file:
                config = json.load(config_file)

            if thread is None:
                return config  # Return entire configuration

            # Search for specific thread's current chunk
            for entry in config:
                if entry["thread_name"] == thread:
                    return entry.get("current_chunk", None)

            print(f"Entry for thread '{thread}' not found.")
            return None

        except Exception as e:
            print(f"Error reading configuration file: {e}")
            return None

    def add_config_entry(self, thread_name, associated_file, tmp_dir, current_chunk):
        """
        Add a new entry to the configuration file.

        Args:
            thread_name (str): The name of the thread to be added.
            associated_file (str): The associated file name for the thread.
            tmp_dir (str): Temporary directory for the thread.
            current_chunk (int): The current chunk number for the thread.
        """
        try:
            # Read existing config data or create a new list if the file doesn't exist
            config_data = self.read_config_file() or []

            # Check if the thread already exists in the configuration
            for entry in config_data:
                if entry["thread_name"] == thread_name:
                    print(
                        f"Thread '{thread_name}' already exists. Use 'update_config_entry' to update it."
                    )
                    return

            # Add the new entry
            config_data.append(
                {
                    "thread_name": thread_name,
                    "associated_file": associated_file,
                    "tmp_dir": tmp_dir,
                    "current_chunk": current_chunk,
                }
            )

            # Save the updated configuration
            self.create_config_file(config_data)

        except Exception as e:
            print(f"Error adding config entry: {e}")

    def update_config_entry(
        self, thread_name, associated_file=None, tmp_dir=None, current_chunk=None
    ):
        """
        Update an existing entry in the configuration file.

        Args:
            thread_name (str): The name of the thread to update.
            associated_file (str, optional): The updated associated file name. Defaults to None.
            tmp_dir (str, optional): The updated temporary directory. Defaults to None.
            current_chunk (int, optional): The updated current chunk number. Defaults to None.
        """
        try:
            # Read existing config data
            config_data = self.read_config_file() or []

            # Find the entry to update
            for entry in config_data:
                if entry["thread_name"] == thread_name:
                    if associated_file:
                        entry["associated_file"] = associated_file
                    if tmp_dir:
                        entry["tmp_dir"] = tmp_dir
                    if current_chunk is not None:
                        entry["current_chunk"] = current_chunk

                    # Save the updated configuration
                    self.create_config_file(config_data)
                    print(f"Thread '{thread_name}' updated successfully.")
                    return True

            print(f"Thread '{thread_name}' not found in the configuration.")

        except Exception as e:
            print(f"Error updating config entry: {e}")
