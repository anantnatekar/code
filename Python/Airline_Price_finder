import time
import json
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd

class FlightPriceFinder:
    def __init__(self, headless=True):
        """Initialize the flight price finder with Chrome WebDriver"""
        self.options = Options()
        if headless:
            self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = None
        self.results = []
    
    def start_driver(self):
        """Start the Chrome WebDriver"""
        try:
            self.driver = webdriver.Chrome(options=self.options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return True
        except Exception as e:
            print(f"Error starting driver: {e}")
            return False
    
    def search_flights(self, origin, destination, departure_date, return_date=None, passengers=1):
        """
        Search for flights on Google Flights
        
        Args:
            origin (str): Origin airport code (e.g., 'JFK', 'LAX')
            destination (str): Destination airport code
            departure_date (str): Departure date in YYYY-MM-DD format
            return_date (str, optional): Return date for round trip
            passengers (int): Number of passengers
        """
        if not self.driver:
            if not self.start_driver():
                return []
        
        try:
            # Build Google Flights URL
            base_url = "https://www.google.com/travel/flights"
            
            # Format dates for URL
            dep_date = departure_date.replace('-', '')
            
            if return_date:
                ret_date = return_date.replace('-', '')
                url = f"{base_url}?tfs=CBwQAhopag0IAxIJL20vMDJfMjg2EgoyMDI0LTEyLTE1agwIAhIIL20vMDE3cjlyBwgBEgNOWUMaCgoCGAESBAhREAEgAQ"
            else:
                url = f"{base_url}?tfs=CBwQARopag0IAxIJL20vMDJfMjg2EgoyMDI0LTEyLTE1cgwIAhIIL20vMDE3cjlyBwgBEgNOWUMgAQ"
            
            print(f"Searching flights from {origin} to {destination} on {departure_date}")
            
            # Navigate to Google Flights
            self.driver.get("https://www.google.com/travel/flights")
            time.sleep(3)
            
            # Fill origin
            self.fill_location_field("origin", origin)
            time.sleep(1)
            
            # Fill destination  
            self.fill_location_field("destination", destination)
            time.sleep(1)
            
            # Set departure date
            self.set_date("departure", departure_date)
            time.sleep(1)
            
            # Set return date if provided
            if return_date:
                self.set_date("return", return_date)
                time.sleep(1)
            
            # Set passengers if not 1
            if passengers != 1:
                self.set_passengers(passengers)
                time.sleep(1)
            
            # Click search
            self.click_search()
            
            # Wait for results and extract them
            return self.extract_flight_results()
            
        except Exception as e:
            print(f"Error during flight search: {e}")
            return []
    
    def fill_location_field(self, field_type, location):
        """Fill origin or destination field"""
        try:
            if field_type == "origin":
                # Click on the origin input
                origin_input = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Where from?']"))
                )
                origin_input.clear()
                origin_input.send_keys(location)
                time.sleep(2)
                
                # Select first suggestion
                first_suggestion = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//ul[@role='listbox']//li[1]"))
                )
                first_suggestion.click()
                
            elif field_type == "destination":
                # Click on destination input
                dest_input = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Where to?']"))
                )
                dest_input.clear()
                dest_input.send_keys(location)
                time.sleep(2)
                
                # Select first suggestion
                first_suggestion = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//ul[@role='listbox']//li[1]"))
                )
                first_suggestion.click()
                
        except Exception as e:
            print(f"Error filling {field_type} field: {e}")
    
    def set_date(self, date_type, date_str):
        """Set departure or return date"""
        try:
            # Click on date field
            if date_type == "departure":
                date_button = self.driver.find_element(By.XPATH, "//input[@placeholder='Departure']")
            else:
                date_button = self.driver.find_element(By.XPATH, "//input[@placeholder='Return']")
            
            date_button.click()
            time.sleep(1)
            
            # Navigate to correct month/year and select date
            # This is a simplified version - you might need to add month/year navigation
            target_date = datetime.strptime(date_str, '%Y-%m-%d')
            day = target_date.day
            
            # Find and click the day
            day_element = self.driver.find_element(By.XPATH, f"//div[@data-iso='{date_str}']")
            day_element.click()
            
        except Exception as e:
            print(f"Error setting {date_type} date: {e}")
    
    def set_passengers(self, count):
        """Set number of passengers"""
        try:
            # Click passenger selector
            passenger_button = self.driver.find_element(By.XPATH, "//button[@aria-label='Passengers']")
            passenger_button.click()
            time.sleep(1)
            
            # Adjust passenger count
            current_count = 1
            while current_count < count:
                plus_button = self.driver.find_element(By.XPATH, "//button[@aria-label='Increase adults']")
                plus_button.click()
                current_count += 1
                time.sleep(0.5)
            
            # Close passenger selector
            done_button = self.driver.find_element(By.XPATH, "//button[text()='Done']")
            done_button.click()
            
        except Exception as e:
            print(f"Error setting passengers: {e}")
    
    def click_search(self):
        """Click the search button"""
        try:
            search_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Search']"))
            )
            search_button.click()
            
            # Wait for results to load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-testid='flight-card']"))
            )
            
        except Exception as e:
            print(f"Error clicking search or waiting for results: {e}")
    
    def extract_flight_results(self):
        """Extract flight information from results page"""
        flights = []
        
        try:
            time.sleep(5)  # Wait for all results to load
            
            # Find all flight cards
            flight_cards = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'pIav2d')]")
            
            for i, card in enumerate(flight_cards[:10]):  # Limit to first 10 results
                try:
                    flight_info = {}
                    
                    # Extract price
                    try:
                        price_element = card.find_element(By.XPATH, ".//span[contains(@aria-label, '$')]")
                        flight_info['price'] = price_element.text
                    except:
                        flight_info['price'] = 'N/A'
                    
                    # Extract airline
                    try:
                        airline_element = card.find_element(By.XPATH, ".//div[contains(@class, 'sSHqwe')]")
                        flight_info['airline'] = airline_element.text
                    except:
                        flight_info['airline'] = 'N/A'
                    
                    # Extract duration
                    try:
                        duration_element = card.find_element(By.XPATH, ".//div[contains(text(), 'hr') or contains(text, 'min')]")
                        flight_info['duration'] = duration_element.text
                    except:
                        flight_info['duration'] = 'N/A'
                    
                    # Extract departure time
                    try:
                        departure_element = card.find_element(By.XPATH, ".//span[contains(@aria-label, 'Departure time')]")
                        flight_info['departure_time'] = departure_element.text
                    except:
                        flight_info['departure_time'] = 'N/A'
                    
                    # Extract arrival time
                    try:
                        arrival_element = card.find_element(By.XPATH, ".//span[contains(@aria-label, 'Arrival time')]")
                        flight_info['arrival_time'] = arrival_element.text
                    except:
                        flight_info['arrival_time'] = 'N/A'
                    
                    # Extract stops
                    try:
                        stops_element = card.find_element(By.XPATH, ".//span[contains(text(), 'stop') or contains(text(), 'nonstop')]")
                        flight_info['stops'] = stops_element.text
                    except:
                        flight_info['stops'] = 'N/A'
                    
                    flights.append(flight_info)
                    
                except Exception as e:
                    print(f"Error extracting info from flight card {i}: {e}")
                    continue
            
            return flights
            
        except Exception as e:
            print(f"Error extracting flight results: {e}")
            return []
    
    def find_best_prices(self, routes, date_range_days=7):
        """
        Find best prices for multiple routes over a date range
        
        Args:
            routes (list): List of tuples (origin, destination)
            date_range_days (int): Number of days to check from today
        """
        all_results = []
        
        start_date = datetime.now() + timedelta(days=1)  # Start tomorrow
        
        for route in routes:
            origin, destination = route
            print(f"\nSearching route: {origin} -> {destination}")
            
            for day_offset in range(date_range_days):
                search_date = start_date + timedelta(days=day_offset)
                date_str = search_date.strftime('%Y-%m-%d')
                
                print(f"  Checking date: {date_str}")
                
                flights = self.search_flights(origin, destination, date_str)
                
                for flight in flights:
                    flight['route'] = f"{origin} -> {destination}"
                    flight['date'] = date_str
                    all_results.append(flight)
                
                time.sleep(2)  # Be respectful with requests
        
        return all_results
    
    def save_results(self, results, filename='flight_results.csv'):
        """Save results to CSV file"""
        if results:
            df = pd.DataFrame(results)
            df.to_csv(filename, index=False)
            print(f"Results saved to {filename}")
        else:
            print("No results to save")
    
    def display_best_deals(self, results, top_n=5):
        """Display the best flight deals"""
        if not results:
            print("No flight results to display")
            return
        
        # Filter out results without valid prices
        valid_results = [r for r in results if r.get('price', 'N/A') != 'N/A']
        
        if not valid_results:
            print("No valid price results found")
            return
        
        # Sort by price (assuming price format like '$XXX')
        try:
            sorted_results = sorted(valid_results, 
                                  key=lambda x: float(x['price'].replace('$', '').replace(',', '')))
        except:
            sorted_results = valid_results
        
        print(f"\n🎯 TOP {top_n} BEST FLIGHT DEALS:")
        print("-" * 80)
        
        for i, flight in enumerate(sorted_results[:top_n], 1):
            print(f"{i}. {flight.get('route', 'N/A')} - {flight.get('date', 'N/A')}")
            print(f"   💰 Price: {flight.get('price', 'N/A')}")
            print(f"   ✈️  Airline: {flight.get('airline', 'N/A')}")
            print(f"   🕐 Duration: {flight.get('duration', 'N/A')}")
            print(f"   🛫 Departure: {flight.get('departure_time', 'N/A')}")
            print(f"   🛬 Arrival: {flight.get('arrival_time', 'N/A')}")
            print(f"   🔄 Stops: {flight.get('stops', 'N/A')}")
            print("-" * 40)
    
    def close(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()

# Example usage
def main():
    # Initialize the flight finder
    finder = FlightPriceFinder(headless=False)  # Set to True to run in background
    
    try:
        # Example: Search for specific flight
        print("Searching for flights...")
        
        # Single flight search
        flights = finder.search_flights(
            origin="JFK",
            destination="LAX", 
            departure_date="2024-12-20",
            return_date="2024-12-27",
            passengers=1
        )
        
        print(f"Found {len(flights)} flights")
        finder.display_best_deals(flights)
        
        # Multiple routes over date range
        routes = [
            ("JFK", "LAX"),
            ("JFK", "SFO"),
            ("LGA", "LAX")
        ]
        
        # Uncomment to search multiple routes
        # all_results = finder.find_best_prices(routes, date_range_days=3)
        # finder.display_best_deals(all_results, top_n=10)
        # finder.save_results(all_results)
        
    except Exception as e:
        print(f"Error in main execution: {e}")
    
    finally:
        finder.close()

if __name__ == "__main__":
    main()
