def scrape_goodreads_reviews(book_url, output_file="goodreads_reviews.csv"):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    print(f"Requesting data from: {book_url}")
    try:
        response = requests.get(book_url, headers=headers, timeout=15)
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    if response.status_code != 200:
        print(f"HTTP Error {response.status_code}: Goodreads may be throttling or blocking the request.")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # <article class="ReviewCard"> or 'div.review' (older layouts)
    review_elements = soup.select('article.ReviewCard') or soup.select('div.review')
    
    print(f"Found {len(review_elements)} potential review containers on this page layer.")
    reviews_found = []
    
    for element in review_elements:
        # Extract the reviewer name
        name_elem = element.select_one('.ReviewerProfile__name') or element.select_one('a.user')
        reviewer_name = name_elem.text.strip() if name_elem else "Anonymous"
        
        # Extract content
        text_elem = element.select_one('.ReviewText__content') or element.select_one('.reviewText')
        review_text = text_elem.text.strip() if text_elem else ""
        
        if review_text:
            # Clean white spaces and newline breaks
            cleaned_text = " ".join(review_text.split())
            
            # Validation check to filter out empty strings or text placeholders
            if len(cleaned_text) > 10:
                reviews_found.append({
                    "Reviewer": reviewer_name,
                    "Review": cleaned_text
                })

    # Save to CSV
    if reviews_found:
        with open(output_file, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["Reviewer", "Review"])
            writer.writeheader()
            writer.writerows(reviews_found)
        print(f"🎉 Success! Saved {len(reviews_found)} cleaned reviews into '{output_file}'.")
    else:
        print("❌ No reviews could be parsed.")
        print("Reason: The text is likely hidden behind client-side JavaScript.")
# End of function


# Test
if __name__ == "__main__":
    # URL targeting the main edition entry for Ivo Andrić's Prokleta Avlija
    target_url = "https://www.goodreads.com/book/show/11553583-prokleta-avlija"
    scrape_goodreads_reviews(target_url)
