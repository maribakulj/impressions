"""The chains of layers used in the experiments (stage 0 = the museum image as given)."""

CHAINS: dict[str, list[str]] = {
    "frame": ["gilt_frame"],
    "mat": ["mat_border"],
    "wall": ["gilt_frame", "museum_wall"],
    "book": ["book_page", "book_photo"],
    "web": ["screenshot_ui", "screen_photo"],
    "print": ["halftone_print", "rephotograph"],
    "deep": ["gilt_frame", "museum_wall", "book_page", "book_photo", "screenshot_ui",
             "screen_photo"],
    # controls: as much reduction / pixel damage as a frame, but no frame
    "ctrl_shrink": ["shrink_neutral"],
    "ctrl_jpeg": ["jpeg_resample"],
}
