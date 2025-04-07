# filemac
A python file `conversion`, `manipulation`, `Analysis` toolkit
`This is a Linux command-line interface (CLI) utility that coverts documents from one format to another,
analyzes files, manipulates files.
Your can also convert text file to mp3 format using google Text to speech library (gTTS).`
## Name variations
```shell
   filemac -h
   Filemac -h
   FILEMAC -h
   ```

## Installation
1. using pip

   ```shell
	pip install filemac
   ```
2. Install from github

    ```shell
    pip install git+https://github.com/skye-cyber/FileMAC.git
    ```
## Usage

To run the CLI app, use the following command:

```shell
FileMAC [options] stdin format
```

Replace `[options]` with the appropriate command-line options based on the functionality you want to execute.

## Available Options
``*``
- `1`:  --convert_doc         (doc* inter-conversion + tts)
- `2`:  --convert_audio
- `3`:  --convert_video
- `4`:  --convert_image
- `5`:  --extract_audio
- `6`:  --Analyze_video
- `8`:  --OCR
- `9`:  --convert_doc2image
- `10`: --extract_audio
- `11`: --AudioJoin (join audio files to one master file)
- `12`: --resize_image
- `13`: --doc_long_image      (convert pdf/doc/docx to long image)
- `14`: --image2pdf (convert image(s) to pdf)
- `15`: --image2word (convert image(s) to word document)
- `16`: --image2gray (convert image(s) to grayscale)
- `17`: --extract_pages (extract pages from pdf selectively)
- `18`: --scanAsImg (convert pdf to images then extract text, number of images=number of pages)
- `19`: --scanAsLong_Image (convert pdf to long image then extract text-good for continuous text extraction)
- `20`: --pdfjoin
- `21`: --audio_effect (manipulate audio/video voice)
- `22`: --voicetype (voice typing) - upcoming

## Examples

1. Example command 1:

   ```shell
   filemac --convert_doc example.docx -t pdf
   ```
    **Supported formats For document conversion**
       `1`.  PDF to (word, txt, audio\[tts\]) 
       `2`.  PDF to TXT
       `3`.  PDF to Audio(ogg,mp3,wav..*)
       `4`.  DOCX to (PDF, pptx/ppt, txt, audio,
       `5`.  TXT to (PDF, word, audio)
       `6`. PPTX to DOCX
       `7`. XLSX to (Sql, CSV, TXT, word)


    This promt parses convert_doc signifying that the inteded operation id document conversion then parses ```example.docx``` as the input file(file path can also be provided) to be converted to format ```pdf```.
the output file assumes the base name of the input file but the extension conforms to the parsed format```pdf```

2. converting text mp3 to wav
   ```shell
   filemac --convert_audio example.mp3 -t wav
    ```
    **Supported formats For audio conversion**
    - (``wav, mp3, ogg, flv, ogv, avi, mkv, mov, webm``)


3. Extract text from images
    ```shell
    filemac --OCR image.jpg
    ```

4. converting videos
   ```shell
   filemac --convert_video example.mp4 -t wav
    ```
    **Supported formats For video conversion**
    (``mp4, avi, ogv, webm, mov, mkv, flv, wmv``)


5. converting images
   ```shell
   filemac --convert_image example.png -t jpg
    ```
#### Supported formats For audio conversion
       `1`.JPEG: `.jpg`
       `2`.PNG": `.png`
       `3`.GIF": `.gif`
       `4`.BM":  `.bmp`
       `5`.TIFF: `.tiff`
       `6`.EXR   `.exr`
       `7`.PDF:  `.pdf`
       `8`.WebP: `.webp`
       `9`.ICNS: `.icns`
       `10`.PSD: `.psd`
       `11`.SVG: `.svg`
       `12`.EPS: `.eps`


### Manipulate audio
---
#### Audio 
```shell
filemac --audio_effect 'demo.mp3' --effect high
```

**Original**<br/>
  [Listen to Original Audio](https://skye-cyber.github.io/FileMAC/res/demo.html)

**Result**<br/>
  [Listen to Modified Audio](https://skye-cyber.github.io/FileMAC/res/demo.html)
  
---

#### Video
```shell
filemac --audio_effect 'demo.mp4' --effect high
```
**Original**<br/>
  [Listen to Original Video](https://skye-cyber.github.io/FileMAC/res/demo.html)
  
**Result**<br/>
  [Listen to Modified Video](https://skye-cyber.github.io/FileMAC/res/demo.html)
  
---

## Help
in any case you can pass the string help to an option to see its supported operations or inputs nd output formats.
```shell
   filemac --convert_doc help
```
The above command displays the surported input and output formats for document conversion.
## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License
This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.


Feel free to modify and customize this template according to your specific project requirements and add any additional sections or information that you think would be helpful for users.

