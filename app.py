import ollama
import json
import sys
from flask import Flask, request, jsonify

class FinancialAssistant:
    def __init__(self, model="deepseek-r1:14b"):
        """
        Initialize the financial assistant with a specified Ollama model.
        
        Args:
            model (str): The Ollama model to use for financial analysis.
        """
        try:
            # Verify the model is available in Ollama
            ollama.list()
            self.model = model
        except Exception as e:
            print(f"Error initializing model: {e}")
            print("Please ensure Ollama is running and the model is installed.")
            sys.exit(1)

        # Comprehensive sector benchmarks (same as previous implementation)
        self.sector_benchmarks = {
           "Banks and NBFC": {
                "key_ratios": {
                    "NIM": {"min": 3.0, "weight": 0.2},
                    "ROA": {"min": 1.5, "weight": 0.2},
                    "ROE": {"min": 15.0, "weight": 0.3},
                    "Gross NPA": {"max": 3.0, "weight": -0.2},
                    "CAR": {"min": 12.0, "weight": 0.1},
                    "P/B Ratio": {"max": 3.0, "weight": 0}
                },
                "growth_formula": lambda data: (
                    (0.3 * data.get("ROE", 0)) + 
                    (0.2 * data.get("ROA", 0)) + 
                    (0.2 * data.get("NIM", 0)) - 
                    (0.2 * data.get("Gross NPA", 0)) + 
                    (0.1 * data.get("CAR", 0))
                )
            },
            "IT & Technology": {
                "key_ratios": {
                    "Revenue Growth": {"min": 12.0, "weight": 0.25},
                    "Operating Margin": {"min": 20.0, "weight": 0.25},
                    "FCF Margin": {"min": 15.0, "weight": 0.25},
                    "ROE": {"min": 20.0, "weight": 0.25},
                    "P/E Ratio": {"max": 30.0, "weight": 0},
                    "EV/EBITDA": {"max": 15.0, "weight": 0}
                },
                "growth_formula": lambda data: (
                    (0.25 * data.get("Revenue Growth", 0)) + 
                    (0.25 * data.get("Operating Margin", 0)) + 
                    (0.25 * data.get("FCF Margin", 0)) + 
                    (0.25 * data.get("ROE", 0))
                )
            },
            "FMCG & Consumer Goods": {
                "key_ratios": {
                    "Revenue Growth": {"min": 8.0, "weight": 0.25},
                    "Gross Margin": {"min": 50.0, "weight": 0.15},
                    "ROE": {"min": 18.0, "weight": 0.2},
                    "Debt-to-Equity": {"max": 0.5, "weight": -0.2},
                    "Dividend Yield": {"min": 1.5, "weight": 0.05},
                    "P/E Ratio": {"max": 40.0, "weight": 0}
                },
                "growth_formula": lambda data: (
                    (0.25 * data.get("Revenue Growth", 0)) + 
                    (0.15 * data.get("Gross Margin", 0)) + 
                    (0.2 * data.get("ROE", 0)) - 
                    (0.2 * data.get("Debt-to-Equity", 0)) + 
                    (0.05 * data.get("Dividend Yield", 0))
                )
            },
            "Automobiles": {
                "key_ratios": {
                    "Revenue Growth": {"min": 10.0, "weight": 0.25},
                    "Operating Margin": {"min": 12.0, "weight": 0.3},
                    "Debt-to-Equity": {"max": 1.0, "weight": -0.2},
                    "ROE": {"min": 15.0, "weight": 0.25},
                    "P/FCF": {"max": 20.0, "weight": 0}
                },
                "growth_formula": lambda data: (
                    (0.3 * data.get("Operating Margin", 0)) + 
                    (0.25 * data.get("ROE", 0)) - 
                    (0.2 * data.get("Debt-to-Equity", 0)) + 
                    (0.25 * data.get("Revenue Growth", 0))
                )
            },
            "Energy, Oil & Gas": {
                "key_ratios": {
                    "EBITDA Margin": {"min": 25.0, "weight": 0.3},
                    "Debt-to-Equity": {"max": 1.2, "weight": -0.2},
                    "Interest Coverage Ratio": {"min": 4.0, "weight": 0.3},
                    "P/FCF": {"max": 15.0, "weight": 0},
                    "Dividend Yield": {"min": 3.0, "weight": 0.2}
                },
                "growth_formula": lambda data: (
                    (0.3 * data.get("EBITDA Margin", 0)) - 
                    (0.2 * data.get("Debt-to-Equity", 0)) + 
                    (0.3 * data.get("Interest Coverage Ratio", 0)) + 
                    (0.2 * data.get("Dividend Yield", 0))
                )
            },
            "Healthcare & Pharmaceuticals": {
                "key_ratios": {
                    "Revenue Growth": {"min": 10.0, "weight": 0.25},
                    "Operating Margin": {"min": 18.0, "weight": 0.2},
                    "ROE": {"min": 16.0, "weight": 0.2},
                    "R&D Expenditure": {"min": 5.0, "weight": 0.2},
                    "P/E Ratio": {"max": 35.0, "weight": 0}
                },
                "growth_formula": lambda data: (
                    (0.25 * data.get("Revenue Growth", 0)) + 
                    (0.2 * data.get("Operating Margin", 0)) + 
                    (0.2 * data.get("ROE", 0)) + 
                    (0.2 * data.get("EBITDA Growth", 0)) + 
                    (0.15 * data.get("Free Cash Flow Growth", 0))
                )
            },
            "Retail Sector": {
                "key_ratios": {
                    "Revenue Growth": {"min": 8.0, "weight": 0.3},
                    "Operating Margin": {"min": 10.0, "weight": 0.2},
                    "ROE": {"min": 12.0, "weight": 0.15},
                    "Debt-to-Equity": {"max": 1.0, "weight": -0.15},
                    "Free Cash Flow Growth": {"min": 10.0, "weight": 0.2}
                },
                "growth_formula": lambda data: (
                    (0.3 * data.get("Revenue Growth", 0)) + 
                    (0.2 * data.get("Operating Margin", 0)) + 
                    (0.15 * data.get("ROE", 0)) - 
                    (0.15 * data.get("Debt-to-Equity", 0)) + 
                    (0.2 * data.get("Free Cash Flow Growth", 0))
                )
            }
        }

    def stock_analysis(self, financial_data, sector):
        """
        Comprehensive stock analysis with sector-specific benchmarks.
        
        Args:
            financial_data (dict): Dictionary of financial metrics
            sector (str): The sector of the stock
        
        Returns:
            dict: Detailed stock analysis report
        """
        try:
            # Validate sector
            if sector not in self.sector_benchmarks:
                return {
                    "error": "Sector not recognized", 
                    "available_sectors": list(self.sector_benchmarks.keys())
                }
            
            # Get sector-specific benchmarks
            sector_benchmarks = self.sector_benchmarks[sector]
            
            # Calculate growth score
            growth_score = sector_benchmarks["growth_formula"](financial_data)
            
            # Evaluate key ratios
            ratio_analysis = []
            meets_benchmark = True
            
            for ratio, details in sector_benchmarks["key_ratios"].items():
                value = financial_data.get(ratio)
                
                # Check if value exists
                if value is None:
                    ratio_analysis.append(f"⚠️ {ratio}: Not provided in financial data")
                    meets_benchmark = False
                    continue
                
                # Minimum value check
                if "min" in details:
                    if value < details["min"]:
                        ratio_analysis.append(f"❌ {ratio}: {value} (Below benchmark of {details['min']})")
                        meets_benchmark = False
                    else:
                        ratio_analysis.append(f"✅ {ratio}: {value} (Meets benchmark of {details['min']})")
                
                # Maximum value check
                if "max" in details:
                    if value > details["max"]:
                        ratio_analysis.append(f"❌ {ratio}: {value} (Above benchmark of {details['max']})")
                        meets_benchmark = False
                    else:
                        ratio_analysis.append(f"✅ {ratio}: {value} (Meets benchmark of {details['max']})")
            
            # Prepare comprehensive prompt for AI-generated analysis
            prompt = f"""
Provide a comprehensive stock analysis for a company in the {sector} sector.

Financial Data:
{json.dumps(financial_data, indent=2)}

Growth Score: {growth_score:.2f}

Key Analysis Points:
1. Interpret the growth score
2. Evaluate the company's performance against sector benchmarks
3. Provide investment insights for a beginner in detail
4. Highlight potential strengths and weaknesses
5. Suggest areas of further investigation

Key Ratio Analysis:
{chr(10).join(ratio_analysis)}

Overall Benchmark Status: {"Meets Most Benchmarks" if meets_benchmark else "Does Not Meet All Benchmarks"}
"""
            
            # Generate detailed analysis using Ollama
            analysis_response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
            
            return {
                "sector": sector,
                "growth_score": growth_score,
                "ratio_performance": ratio_analysis,
                "ai_analysis": analysis_response['message']['content'],
                "meets_benchmark": meets_benchmark
            }
        
        except Exception as e:
            return {"error": f"Error performing stock analysis: {str(e)}"}

# Initialize Flask app and Financial Assistant
app = Flask(__name__)
financial_assistant = FinancialAssistant()

@app.route('/analyze_stock', methods=['POST'])
def analyze_stock():
    """
    Flask route for stock analysis.
    
    Expected JSON input:
    {
        "financial_data": {...},
        "sector": "Banks and NBFC"
    }
    """
    # Check if JSON data is present
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    # Parse input data
    data = request.get_json()
    
    # Validate required fields
    if 'financial_data' not in data or 'sector' not in data:
        return jsonify({
            "error": "Missing required fields",
            "required_fields": ["financial_data", "sector"]
        }), 400
    
    # Perform stock analysis
    analysis_result = financial_assistant.stock_analysis(
        data['financial_data'], 
        data['sector']
    )
    
    # Check if analysis returned an error
    if 'error' in analysis_result:
        return jsonify(analysis_result), 400
    
    return jsonify(analysis_result)

@app.route('/available_sectors', methods=['GET'])
def get_available_sectors():
    """
    Returns list of available sectors for stock analysis.
    """
    return jsonify({
        "sectors": list(financial_assistant.sector_benchmarks.keys())
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)