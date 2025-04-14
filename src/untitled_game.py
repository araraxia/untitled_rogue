#!/usr/bin/env python3

from untitled_gameapp import Untgap
import tkinter as tk

class UntGame(Untgap):
    def __init__(self):
        Untgap.logger.debug("Initializing UntGame.")        

         
    ### Game Frames ###
    def pack_game_frames(self, game_frames):
        Untgap.logger.debug("Packing game frames.")

        header_frame = game_frames["header"]["inner"]
        header_border = game_frames["header"]["border"]
        body_frame = game_frames["body"]["inner"]
        body_border = game_frames["body"]["border"]
        footer_frame = game_frames["footer"]["inner"]
        footer_border = game_frames["footer"]["border"]

        header_border.pack(
            side="top", fill="x", padx=Untgap.frame_pad, pady=Untgap.frame_pad
        )
        header_frame.pack(side="top", fill="x")

        body_border.pack(
            side="top",
            fill="both",
            expand=True,
            padx=Untgap.frame_pad,
            pady=Untgap.frame_pad,
        )
        body_frame.pack(side="top", fill="both", expand=True)

        footer_border.pack(
            side="bottom", fill="x", padx=Untgap.frame_pad, pady=Untgap.frame_pad
        )
        footer_frame.pack(side="bottom", fill="x")

    def create_frame(self, **kwargs):
        Untgap.logger.debug("Creating frame objects.")
        border_frame = tk.Frame(
            Untgap.root,
            bg=Untgap.frame_color,
            borderwidth=Untgap.border_thickness,
            relief=Untgap.frame_relief,
            **kwargs,
        )

        inner_frame = tk.Frame(border_frame, bg=Untgap.bg, **kwargs)

        frame = {"inner": inner_frame, "border": border_frame}

        return frame

    def init_frames(self, font_height, head_pady, foot_pady):
        Untgap.logger.debug("Initializing frames.")

        Untgap.logger.debug(f"Initializing header frame.")
        header_frame = self.create_frame(height=(font_height + head_pady))

        Untgap.logger.debug(f"Initializing body frame.")
        body_frame = self.create_frame()

        Untgap.logger.debug(f"Initializing footer frame.")
        footer_frame = self.create_frame(height=(font_height + foot_pady))

        game_frames = {
            "header": header_frame,
            "body": body_frame,
            "footer": footer_frame,
        }

        return game_frames

        
    def run(self): ...