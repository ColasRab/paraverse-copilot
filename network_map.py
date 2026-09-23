
import json

import httpx
from fastmcp import FastMCP
import network_map

mcp = FastMCP("Paraverse Copilot")

PARAVERSE_API = "https://paraverse.feutech.edu.ph/api/v1"

def parse_cookie_string(cookie_str: str) -> dict:
    return dict(
        pair.split("=", 1)
        for pair in cookie_str.split("; ")
        if "=" in pair
    )


COOKIES = parse_cookie_string("visid_incap_3240127=LDGSb7/tSCOnFOJa8PiYXvKUAmoAAAAAQUIPAAAAAAACMqDHBk2xY18aRZWgGNwH; _ga=GA1.1.1296788114.1778554102; visid_incap_3212400=IYGXdJinQj2z9re/oyrsqyjeC2oAAAAAQUIPAAAAAAAhGvI0rbInjwQaVAj+w2kd; visid_incap_3210166=PeVKq2zESpGvYi9buIwV2v03Q2oAAAAAQUIPAAAAAABCiPd7vOKAW755xMKh0Njp; _ga_2DRTF343F8=GS2.1.s1790077119$o29$g0$t1790077119$j60$l0$h0; mbg=06dv5td4sm3d6mvg377iprbr2f; incap_ses_1635_3240127=h3HFWSDnAUi3awcKhbCwFrVAs2oAAAAADT+6kTeF+nZRMH6fksS4lw==; incap_ses_1633_3240127=kOSvIGnrS22EgCvDh5WpFj6bs2oAAAAAd7/GE5vRFUKgI0vpRLAlhg==; remember_me_cookie=976b67fb8726de2f2ff02b310d7ded1a96c4b5d777278ceecea85e6331ced9fa; _ga_SR6Q4GLJJH=GS2.1.s1790155598$o50$g1$t1790156165$j59$l0$h0")

async def fetch_module(code: str) -> str:
    async with httpx.AsyncClient(base_url=f"{PARAVERSE_API}/network-map", cookies=COOKIES) as client:
        try:
            response = await client.get("course-view", params={"code": code})
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"Error fetching module {code}: {e.response.status_code} - {e.response.text}")
            return {}

async def fetch_leaderboard_classes() -> str:
    async with httpx.AsyncClient(base_url=f"{PARAVERSE_API}", cookies=COOKIES) as client:
        try:
            response = await client.get("/leaderboard/browse?my_classes=true")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"Error fetching leaderboard classes: {e.response.status_code} - {e.response.text}")
            return {}


@mcp.tool(
    name="find_module",
    description="Fetches the details of a course from the Paraverse API."
)
async def find_module(module_name: str) -> dict:
    data = await fetch_module(module_name)
    if not data:
        return f"Module {module_name} not found."
    
    return data;

@mcp.tool(
    name="get_leaderboard_classes",
    description="Fetches all active classes from the Paraverse API."
)
async def get_leaderboard_classes() -> dict:
    data = await fetch_leaderboard_classes()
    if not data:
        return "No leaderboard classes found."
    
    return data;


if "__name__" == "__main__":
    mcp.run()