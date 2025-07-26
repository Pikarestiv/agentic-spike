import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {  
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    if city.lower() == "amawbia":
        return {  
            "status": "success",
            "report": (
                "The weather for {city} dey sunny o with a temperature wey dey up to 32 degrees"
                " Celsius."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }


    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}


def convert_temperature(temperature: float, from_unit: str, to_unit: str) -> dict:
    """Converts temperature between Celsius, Fahrenheit, and Kelvin.

    Args:
        temperature (float): The temperature value to convert.
        from_unit (str): Source unit ('C', 'F', or 'K').
        to_unit (str): Target unit ('C', 'F', or 'K').

    Returns:
        dict: status and result or error msg.
    """
    from_unit, to_unit = from_unit.upper(), to_unit.upper()
    
    if from_unit not in ['C', 'F', 'K'] or to_unit not in ['C', 'F', 'K']:
        return {"status": "error", "error_message": "Invalid unit. Use 'C', 'F', or 'K'."}
    
    if from_unit == to_unit:
        result = temperature
    else:
        # Convert to Celsius first
        celsius = temperature if from_unit == 'C' else (temperature - 32) * 5/9 if from_unit == 'F' else temperature - 273.15
        # Convert to target unit
        result = celsius if to_unit == 'C' else celsius * 9/5 + 32 if to_unit == 'F' else celsius + 273.15
    
    return {"status": "success", "report": f"{temperature}°{from_unit} is {result:.2f}°{to_unit}"}
  
def get_city_timezone(city: str) -> dict:
  """Returns the timezone for a specified city.

  Args:
      city (str): The name of the city.

  Returns:
      dict: status and result or error msg.
  """
  timezones = {
      "new york": "America/New_York (UTC-5/-4)",
      "amawbia": "Africa/Lagos (UTC+1)",
      "london": "Europe/London (UTC+0/+1)",
      "tokyo": "Asia/Tokyo (UTC+9)"
  }
  
  city_lower = city.lower()
  if city_lower in timezones:
      return {
          "status": "success",
          "report": f"The timezone for {city} is {timezones[city_lower]}."
      }
  else:
      return {
          "status": "error",
          "error_message": f"Timezone information for '{city}' is not available."
      }
      
def add_two_numbers(num1: int, num2: int) -> dict:
  """Adds two numbers and returns the sum.

  Args:
      num1 (int): The first number
      num2 (int): The second number

  Returns:
      dict: status and result
  """
  
  res = num1 + num2
  if num1.is_integer() and num2.is_integer():
      return {
          "status": "success",
          "result": f"The result  is {res}."
      }
  else:
      return {
          "status": "error",
          "error_message": f"Please enter valid numbers"
      }




root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to answer questions about the time, integer addition, and weather in a city."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time, integer addition, and weather in a city. You must respond with the give response format in the tool function"
    ),
    tools=[get_weather, get_current_time, get_city_timezone, add_two_numbers],
)