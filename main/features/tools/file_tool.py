import base64
from pkg_resources import resource_string

from main.common.constants.test_file_map import *


def get_base64_representation(file_name):
    resource = resource_string(RESOURCES_TEST_FILES, file_name)
    image_64_encode = base64.b64encode(resource)
    return image_64_encode.decode(encoding="utf-8")


PROFILE_IMAGES = {
    PROFILE_IMAGE_DEFAULT: {
        "original_filename": PROFILE_IMAGE_DEFAULT,
        "converted_to_png_file_name": None,
        "base64_content": get_base64_representation(PROFILE_IMAGE_DEFAULT),
        "content_type": "image/png",
        "width": 300,
        "height": 300,
        "size": 15565,
    },
    PROFILE_IMAGE_WBMP: {
        "original_filename": PROFILE_IMAGE_WBMP,
        "converted_to_png_file_name": None,
        "base64_content": get_base64_representation(PROFILE_IMAGE_WBMP),
        "content_type": "image/tiff",
        "width": 3388,
        "height": 1621,
        "size": 153050,
    },
    OVERSIZE_PROFILE_IMAGE_TIFF: {
        "original_filename": OVERSIZE_PROFILE_IMAGE_TIFF,
        "converted_to_png_file_name": None,
        "base64_content": get_base64_representation(OVERSIZE_PROFILE_IMAGE_TIFF),
        "content_type": "image/tiff",
        "width": 3388,
        "height": 1621,
        "size": 203075,
    },
    PROFILE_IMAGE_SVG: {
        "original_filename": PROFILE_IMAGE_SVG,
        "converted_to_png_file_name": None,
        "base64_content": get_base64_representation(PROFILE_IMAGE_SVG),
        "content_type": "image/svg",
        "width": 3388,
        "height": 1621,
        "size": 203075,
    },
    PROFILE_IMAGE_PNG: {
        "original_filename": PROFILE_IMAGE_PNG,
        "converted_to_png_file_name": PROFILE_IMAGE_PNG_PNG,
        "base64_content": get_base64_representation(PROFILE_IMAGE_PNG),
        "content_type": "image/png",
        "width": 3388,
        "height": 1621,
        "size": 941831,
    },
    PROFILE_IMAGE_PGM: {
        "original_filename": PROFILE_IMAGE_PGM,
        "converted_to_png_file_name": PROFILE_IMAGE_PGM_PNG,
        "base64_content": get_base64_representation(PROFILE_IMAGE_PGM),
        "content_type": "image/x-portable-greymap",
        "width": 3388,
        "height": 1621,
        "size": 5491965,
    },
    PROFILE_IMAGE_PBM: {
        "original_filename": PROFILE_IMAGE_PBM,
        "converted_to_png_file_name": PROFILE_IMAGE_PBM_PNG,
        "base64_content": get_base64_representation(PROFILE_IMAGE_PBM),
        "content_type": "image/x-portable-bitmap",
        "width": 3388,
        "height": 1621,
        "size": 687317,
    },
    PROFILE_IMAGE_ICO: {
        "original_filename": PROFILE_IMAGE_ICO,
        "converted_to_png_file_name": PROFILE_IMAGE_ICO_PNG,
        "base64_content": get_base64_representation(PROFILE_IMAGE_ICO),
        "content_type": "image/x-icon",
        "width": 256,
        "height": 122,
        "size": 128894,
    },
    PROFILE_IMAGE_JPEG: {
        "original_filename": PROFILE_IMAGE_JPEG,
        "converted_to_png_file_name": PROFILE_IMAGE_JPEG_PNG,
        "base64_content": get_base64_representation(PROFILE_IMAGE_JPEG),
        "content_type": "image/jpeg",
        "width": 3388,
        "height": 1621,
        "size": 153050,
    },
    PROFILE_IMAGE_JP2: {
        "original_filename": PROFILE_IMAGE_JP2,
        "converted_to_png_file_name": PROFILE_IMAGE_JP2_PNG,
        "base64_content": get_base64_representation(PROFILE_IMAGE_JP2),
        "content_type": "image/jp2",
        "width": 3388,
        "height": 1621,
        "size": 942839,
    },
}


TEST_FILES = {
    "base64_avi_1280_1_5mg": {
        "original_filename": FILE_AVI_1280_1_5MG,
        "content_type": "video/x-msvideo",
        "base64_content": get_base64_representation(FILE_AVI_1280_1_5MG),
    },
    "base64_csv_5000rows": {
        "original_filename": FILE_CSV_5000ROWS,
        "content_type": "text/plain",  # "text/csv",
        "base64_content": get_base64_representation(FILE_CSV_5000ROWS),
    },
    "base64_docx_100kb": {
        "original_filename": FILE_DOCX_100KB,
        "content_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        # "application/msword",
        "base64_content": get_base64_representation(FILE_DOCX_100KB),
    },
    "base64_doc_100kb": {
        "original_filename": FILE_DOC_100KB,
        "content_type": "application/CDFV2",  # "application/doc",
        "base64_content": get_base64_representation(FILE_DOC_100KB),
    },
    "base64_gif_500kb": {
        "original_filename": FILE_GIF_500KB,
        "content_type": "image/gif",
        "base64_content": get_base64_representation(FILE_GIF_500KB),
    },
    "base64_html": {
        "original_filename": FILE_HTML,
        "content_type": "text/html",
        "base64_content": get_base64_representation(FILE_HTML),
    },
    "base64_jpg_100kb": {
        "original_filename": FILE_JPG_100KB,
        "content_type": "image/jpeg",
        "base64_content": get_base64_representation(FILE_JPG_100KB),
    },
    "base64_json_1kb": {
        "original_filename": FILE_JSON_1KB,
        "content_type": "text/plain",  # "text/json",
        "base64_content": get_base64_representation(FILE_JSON_1KB),
    },
    "base64_mov_1280_1_4mb": {
        "original_filename": FILE_MOV_1280_1_4MB,
        "content_type": "video/quicktime",
        "base64_content": get_base64_representation(FILE_MOV_1280_1_4MB),
    },
    "base64_mp3_700kb": {
        "original_filename": FILE_MP3_700KB,
        "content_type": "audio/mpeg",
        "base64_content": get_base64_representation(FILE_MP3_700KB),
    },
    "base64_mp4_480_1_5mg": {
        "original_filename": FILE_MP4_480_1_5MG,
        "content_type": "video/mp4",
        "base64_content": get_base64_representation(FILE_MP4_480_1_5MG),
    },
    "base64_odp_200kb": {
        "original_filename": FILE_ODP_200KB,
        "content_type": "application/vnd.oasis.opendocument.presentation",
        "base64_content": get_base64_representation(FILE_ODP_200KB),
    },
    "base64_ods_100": {
        "original_filename": FILE_ODS_100,
        "content_type": "application/vnd.oasis.opendocument.spreadsheet",
        "base64_content": get_base64_representation(FILE_ODS_100),
    },
    "base64_odt_100kb": {
        "original_filename": FILE_ODT_100KB,
        "content_type": "application/vnd.oasis.opendocument.text",
        "base64_content": get_base64_representation(FILE_ODT_100KB),
    },
    "base64_ogg_480_1_7mb": {
        "original_filename": FILE_OGG_480_1_7MB,
        "content_type": "video/ogg",
        "base64_content": get_base64_representation(FILE_OGG_480_1_7MB),
    },
    "base64_pdf": {
        "original_filename": FILE_PDF,
        "content_type": "application/pdf",
        "base64_content": get_base64_representation(FILE_PDF),
    },
    "base64_png": {
        "original_filename": FILE_PNG,
        "content_type": "image/png",
        "base64_content": get_base64_representation(FILE_PNG),
    },
    "base64_ppt_250kb": {
        "original_filename": FILE_PPT_250KB,
        "content_type": "application/CDFV2",
        "base64_content": get_base64_representation(FILE_PPT_250KB),
    },
    "base64_rtf_100kb": {
        "original_filename": FILE_RTF_100KB,
        "content_type": "text/rtf",
        "base64_content": get_base64_representation(FILE_RTF_100KB),
    },
    "base64_svg_30kb": {
        "original_filename": FILE_SVG_30KB,
        "content_type": "image/svg+xml",
        "base64_content": get_base64_representation(FILE_SVG_30KB),
    },
    "base64_tiff_1mb": {
        "original_filename": FILE_TIFF_1MB,
        "content_type": "image/tiff",
        "base64_content": get_base64_representation(FILE_TIFF_1MB),
    },
    "base64_txt": {
        "original_filename": FILE_TXT,
        "content_type": "text/plain",
        "base64_content": get_base64_representation(FILE_TXT),
    },
    "base64_wav_1mg": {
        "original_filename": FILE_WAV_1MG,
        "content_type": "audio/x-wav",
        "base64_content": get_base64_representation(FILE_WAV_1MG),
    },
    "base64_webm_640_1_4mb": {
        "original_filename": FILE_WEBM_640_1_4MB,
        "content_type": "video/webm",
        "base64_content": get_base64_representation(FILE_WEBM_640_1_4MB),
    },
    "base64_webp_500kb": {
        "original_filename": FILE_WEBP_500KB,
        "content_type": "image/webp",
        "base64_content": get_base64_representation(FILE_WEBP_500KB),
    },
    "base64_wmv_480_1_2mb": {
        "original_filename": FILE_WMV_480_1_2MB,
        "content_type": "video/x-ms-asf",  # video/x-ms-wmv
        "base64_content": get_base64_representation(FILE_WMV_480_1_2MB),
    },
    "base64_xlsx_100rows": {
        "original_filename": FILE_XLSX_100ROWS,
        # "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        "content_type": "application/octet-stream",
        "base64_content": get_base64_representation(FILE_XLSX_100ROWS),
    },
    "base64_xls_100rows": {
        "original_filename": FILE_XLS_100ROWS,
        "content_type": "application/CDFV2",  # "application/vnd.ms-excel",
        "base64_content": get_base64_representation(FILE_XLS_100ROWS),
    },
    "base64_xml_24kb": {
        "original_filename": FILE_XML_24KB,
        "content_type": "text/xml",  # "application/xhtml+xml",
        "base64_content": get_base64_representation(FILE_XML_24KB),
    },
    "base64_zip_2mb": {
        "original_filename": FILE_ZIP_2MB,
        "content_type": "application/zip",
        "base64_content": get_base64_representation(FILE_ZIP_2MB),
    },
    "base64_max_upload_size_pdf_10mb": {
        "original_filename": FILE_PDF_10MB,
        "content_type": "application/pdf",
        "base64_content": get_base64_representation(FILE_PDF_10MB),
    },
    "base64_oversize_pdf_20mb": {
        "original_filename": FILE_PDF_20MB,
        "content_type": "application/pdf",
        "base64_content": get_base64_representation(FILE_PDF_20MB),
    },
}

