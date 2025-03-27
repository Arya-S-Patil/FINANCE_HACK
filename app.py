import os
import json
import requests
from dotenv import load_dotenv

class FinancialAnalysisModel:
    def __init__(self):
        """
        Initialize the Financial Analysis Model with Hugging Face Inference API
        """
        # Load environment variables
        load_dotenv()
        
        # Hugging Face API endpoint and headers
        self.api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        self.headers = {
            "Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY', 'API KEY HERE')}",
            "Content-Type": "application/json"
        }
    
    def generate_financial_analysis(self, financial_data):
        """
        Generate a comprehensive financial analysis using Hugging Face API
        """
        try:
            # Prepare financial data as a formatted string
            formatted_data = "\n".join([f"{key}: {value}" for key, value in financial_data.items()])
            
            # Construct prompt
            prompt = f"""You are a financial expert explaining complex financial metrics to a beginner.

Financial Data:
{formatted_data}

Please provide:
1. A simple, easy-to-understand explanation of each key metric
2. Insights into the company's financial health
3. Potential flags or areas of concern
4. Beginner-friendly interpretation of the numbers

Explanation should be:
- Clear and jargon-free
- Structured for easy comprehension
- Highlighting key takeaways"""
            
            # Payload for Hugging Face API
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 1000,
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            }
            
            # Send request to Hugging Face
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            
            # Check response
            if response.status_code == 200:
                analysis = response.json()[0]['generated_text']
                return analysis.split(prompt)[-1].strip()
            else:
                return f"Error: {response.status_code} - {response.text}"
        
        except Exception as e:
            print(f"Analysis generation error: {e}")
            return f"Could not generate analysis. Error: {e}"
    
    def generate_financial_flags(self, financial_data):
        """
        Generate financial flags and potential risks
        """
        flags = []
        
        # Market Cap and Valuation Flags
        market_cap = financial_data.get('Market Cap', '0').replace(',', '').replace('Cr.', '')
        try:
            market_cap = float(market_cap)
            if market_cap < 1000:
                flags.append("Small Market Cap: Potential higher risk")
            elif market_cap > 100000:
                flags.append("Large Market Cap: Potentially stable")
        except ValueError:
            flags.append("Market Cap: Unable to evaluate")
        
        # Stock P/E Ratio Flags
        try:
            pe_ratio = float(financial_data.get('Stock P/E', '0'))
            if pe_ratio > 50:
                flags.append("High P/E Ratio: Potentially overvalued")
            elif pe_ratio < 10:
                flags.append("Low P/E Ratio: Potentially undervalued")
        except ValueError:
            flags.append("P/E Ratio: Unable to evaluate")
        
        # Profitability Flags
        try:
            profit_after_tax = float(financial_data.get('Profit after tax', '0').replace(',', '').replace('Cr.', ''))
            if profit_after_tax < 100:
                flags.append("Low Profit: Potential financial challenges")
        except ValueError:
            flags.append("Profit: Unable to evaluate")
        
        # ROE and ROCE Flags
        try:
            roe = float(financial_data.get('ROE', '0').replace('%', ''))
            roce = float(financial_data.get('ROCE', '0').replace('%', ''))
            
            if roe < 10:
                flags.append("Low Return on Equity: Inefficient capital use")
            if roce < 10:
                flags.append("Low Return on Capital Employed: Inefficient capital allocation")
        except ValueError:
            flags.append("ROE/ROCE: Unable to evaluate")
        
        # Dividend Yield Flag
        try:
            dividend_yield = float(financial_data.get('Dividend Yield', '0').replace('%', ''))
            if dividend_yield < 0.5:
                flags.append("Low Dividend Yield: May not be attractive for income investors")
        except ValueError:
            flags.append("Dividend Yield: Unable to evaluate")
        
        return flags

def main():
    # Sample financial data
    financial_data = {
        "Market Cap": "3,20,366 Cr.",
        "Current Price": "2,006",
        "High / Low": "2,030 / 1,419 /",
        "Stock P/E": "37.4",
        "Book Value": "428",
        "Dividend Yield": "0.05 %",
        "ROCE": "11.7 %",
        "ROE": "15.3 %",
        "Face Value": "1.00",
        "Sales": "1,29,266 Cr.",
        "OPM": "36.7 %",
        "Sales growth 3Years": "22.1 %",
        "Sales growth 5Years": "21.0 %",
        "Profit after tax": "8,574 Cr.",
        "Other Inc Prev Ann": "1.46 Cr.",
        "Chg in DII Hold 3Yr": "2.16 %",
    }
    
    # Create financial analysis model
    model = FinancialAnalysisModel()
    
    # Generate analysis
    analysis = model.generate_financial_analysis(financial_data)
    print("\n=== Financial Analysis ===")
    print(analysis)
    
    # Generate financial flags
    flags = model.generate_financial_flags(financial_data)
    print("\n=== Financial Flags ===")
    for flag in flags:
        print(f"- {flag}")

if __name__ == "__main__":
    main()