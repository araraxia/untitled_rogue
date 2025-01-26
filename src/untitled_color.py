#!/usr/bin/env python3
# Untitled Color Module
# Aria Corona January 25th, 2025
# This module provides functions to manipulate colors

def _reduce_brightness(hex_color, percent):
        # Convert hex color to RGB
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        # Reduce each component by the specified percentage
        r = int(r * (1 - percent / 100))
        g = int(g * (1 - percent / 100))
        b = int(b * (1 - percent / 100))
        
        # Ensure values are within the valid range
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        
        # Convert RGB back to hex
        return f'#{r:02x}{g:02x}{b:02x}'