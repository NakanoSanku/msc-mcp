import asyncio
import base64
import cv2
import numpy as np
from mcp.server.fastmcp import FastMCP
from mcp.types import ImageContent, EmbeddedResource
import adbutils
from msc.adbcap import ADBCap
from msc.droidcast import DroidCast
from msc.minicap import MiniCap
from msc.mumu import MuMuCap

# Initialize FastMCP server
mcp = FastMCP("msc-mcp")

@mcp.tool()
def list_devices() -> list[str]:
    """
    List connected Android devices using adbutils.
    Returns a list of device serials.
    """
    try:
        devices = adbutils.adb.device_list()
        return [d.serial for d in devices]
    except Exception as e:
        return [f"Error listing devices: {str(e)}"]

@mcp.tool()
def get_device_info(device_id: str) -> str:
    """
    Get information about a connected device.
    """
    try:
        device = adbutils.adb.device(serial=device_id)
        props = device.get_properties()
        return f"Model: {props.get('ro.product.model', 'Unknown')}\nSDK: {props.get('ro.build.version.sdk', 'Unknown')}\nManufacturer: {props.get('ro.product.manufacturer', 'Unknown')}"
    except Exception as e:
        return f"Error getting device info: {str(e)}"

@mcp.tool()
def install_droidcast(device_id: str) -> str:
    """
    Install DroidCast on the specified device.
    Required before using 'droidcast' capture method.
    """
    try:
        # DroidCast install is an instance method
        dc = DroidCast(device_id)
        dc.install()
        return "DroidCast installed successfully."
    except Exception as e:
        return f"Error installing DroidCast: {str(e)}"

@mcp.tool()
def capture_screenshot(device_id: str, method: str = "adb") -> ImageContent:
    """
    Capture a screenshot from the specified device.
    
    Args:
        device_id: The serial number of the device (e.g., "emulator-5554").
        method: The capture method to use. Options: "adb", "droidcast", "minicap", "mumu".
                Default is "adb".
                Note: "mumu" requires the device to be a MuMu emulator and might need index instead of serial in some contexts, 
                but msc wrapper usually handles serial if mapped, or we might need to adjust. 
                For this implementation, we assume standard usage.
    
    Returns:
        ImageContent containing the screenshot data.
    """
    
    cap = None
    try:
        if method == "adb":
            cap = ADBCap(device_id)
        elif method == "droidcast":
            cap = DroidCast(device_id)
        elif method == "minicap":
            cap = MiniCap(device_id)
        elif method == "mumu":
            # MuMuCap usually takes an index, but let's check if we can pass serial or if we need to find index.
            # For now, we'll try to parse an integer from device_id if it looks like an index, otherwise warn.
            # Actually, msc.mumu.MuMuCap takes an identifier which is usually an int index.
            # If device_id is "0" or "1", we can convert.
            try:
                idx = int(device_id)
                cap = MuMuCap(idx)
            except ValueError:
                # If not an integer, maybe we can't use MuMuCap easily without mapping serial to index.
                # Fallback or error? Let's error for now to be safe.
                raise ValueError("MuMuCap requires an integer index as device_id (e.g., '0').")
        else:
            raise ValueError(f"Unknown capture method: {method}")

        with cap as c:
            # screencap_raw returns bytes, but we want to ensure we have a valid image format for MCP.
            # MCP ImageContent expects data, mimeType.
            # msc's screencap_raw() usually returns raw pixel data (RGBA) or encoded bytes depending on implementation?
            # Let's look at msc docs again. 
            # "screencap() (返回 OpenCV 图像) 和 screencap_raw() (返回原始字节数据)"
            # OpenCV image is numpy array (BGR).
            
            image_np = c.screencap()
            
            # Encode to PNG for transport
            success, encoded_image = cv2.imencode(".png", image_np)
            if not success:
                raise RuntimeError("Failed to encode image to PNG")
            
            image_bytes = encoded_image.tobytes()
            
            return ImageContent(
                type="image",
                data=base64.b64encode(image_bytes).decode("utf-8"),
                mimeType="image/png"
            )

    except Exception as e:
        # In case of error, we might want to return a text error, but tool signature says ImageContent.
        # FastMCP handles exceptions by returning error to client.
        raise RuntimeError(f"Failed to capture screenshot: {str(e)}")

def serve() -> None:
    """
    Run the FastMCP server on stdio.

    FastMCP.run() manages its own event loop via anyio.run(),
    so this wrapper is intentionally synchronous and should
    not be called from inside another asyncio.run().
    """
    mcp.run()
