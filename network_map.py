
import httpx
from fastmcp import FastMCP
import network_map

mcp = FastMCP("Paraverse Copilot")

NETWORK_MAP_API = "https://paraverse.feutech.edu.ph/api/v1/network-map/"
COOKIES = "visid_incap_3240127=jxzItjJsRlS5up4i4knU8eRGIWoAAAAAQUIPAAAAAAAptjCrU9sH2zktWH0QQmzo; _ga=GA1.1.1869510434.1780618345; visid_incap_3210166=K/vt0olzROWsS4PhX3PLZJOEZ2oAAAAAQUIPAAAAAADkjlNBieCpfS83oWJAZamq; visid_incap_3246990=6lmzGRPNTZ6kEGdGVaqUXX6pgmoAAAAAQUIPAAAAAAAQQnhHp1d352pSsgOWEVYS; mbg=vbmkc6mcvcqq7smav1pgt0tamv; incap_ses_1633_3240127=JFAiFON1VXbBOZLAh5WpFq6/smoAAAAA4+A+4GXFmeDBtvpLsqp09w==; remember_me_cookie=73ae48657763c85bdedd1b352b475c50a130f6a2d6fae39f052233040f4ef202; _ga_SR6Q4GLJJH=GS2.1.s1790102075$o46$g1$t1790103430$j58$l0$h0"

async def fetch_module(code: str) -> dict:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"/course-view?code={code}", cookies=COOKIES)
            response.raise_for_status()
            return response.json() 
        except httpx.HTTPStatusError as e:
            print(f"Error fetching module {code}: {e.response.status_code} - {e.response.text}")
            return {}
        
    

@mcp.tool
async def find_module(module_name: str) -> str:
    data = await fetch_module(module_name)
    if not data:
        return f"Module {module_name} not found."

        
    return f"{data.courses}"


if "__name__" == "__main__":
    mcp.run()