from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape():
    # Prompt the user for the items they want to search for
    searchItems = request.args.get('searchItems')

    # Check if searchItems is None
    if searchItems is None:
        return jsonify({"error": "Missing 'searchItems' parameter"}), 400  # Return a 400 Bad Request status code

    # Replace this URL with the Amazon sg webpage you want to scrape
    url = f"https://www.amazon.sg/s?k={searchItems.replace(' ', '+')}"

    # Send an HTTP request to the webpage and get the HTML content
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all the divs with the specified class name
    divs = soup.select('div[class*="puis-card-container"][class*="s-card-container"][class*="puis-expand-height"][class*="puis-include-content-margin"][class*="puis"][class*="s-latency-cf-section"][class*="puis-card-border"]')

    # Create a list to store the results
    results = []

    # Loop through the divs and extract the product information
    for div in divs:
        try:
            # Try to find the product name
            productName = div.find("span", class_="a-size-base-plus a-color-base a-text-normal").text.strip()
            print(f"Product Name: {productName}")
        except AttributeError:
            productName = "Name Unavailable"

        try:
            # Try to find the product price
            productPrice_raw = div.find("span", class_="a-offscreen").text.strip()
            # Extract only the numeric part of the product price
            productPrice = ''.join(char for char in productPrice_raw if char.isdigit() or char == '.')
            print(f"Product Price: {productPrice}")
        except AttributeError:
            productPrice = "Price Unavailable"

        try:
            # Try to find the product link
            productLink = div.find("a", class_="a-link-normal")["href"]
            print(f"Product Link: {productLink}")
        except AttributeError:
            productLink = "Link Unavailable"

        # Add 'www.Amazon.sg' in front of each link
        productLink = f"www.Amazon.sg{productLink}"

        try:
            # Try to find the product image
            productImage = div.find("img", class_="s-image")["src"]
            print(f"Product Image: {productImage}")
        except AttributeError:
            productImage = "Image Unavailable"

        # Append the product information to the results list
        results.append({
            "productName": productName,
            "productPrice": productPrice,
            "productLink": productLink,
            "productImage": productImage
        })

    # Return the results in JSON format without square brackets
    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(debug=True)
