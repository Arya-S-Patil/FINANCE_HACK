# FINANCE_HACK

[![Watch the video](https://img.youtube.com/vi/Y3YVD_EWiRM/0.jpg)](https://www.youtube.com/watch?v=Y3YVD_EWiRM)
## Overview
Financial Insights Analyzer is an advanced, open-source tool that helps beginners understand complex financial data by providing simplified, easy-to-understand explanations of a company's financial metrics.

## Research-Driven Approach

### Custom Growth Formulas
Our tool features custom-developed growth formulas, meticulously crafted through extensive financial research. Each sector-specific formula uniquely weighs key financial metrics to provide a comprehensive growth assessment:


#### 1. Banks and NBFC Sector

Key Ratios:
- Net Interest Margin (NIM) ≥ 3%
- Return on Assets (ROA) ≥ 1.5%
- Return on Equity (ROE) ≥ 15%
- Gross NPA ≤ 3%
- Capital Adequacy Ratio (CAR) ≥ 12%
- Price-to-Book (P/B) Ratio ≤ 3

Growth Score Formula:
```
Growth Score = (0.3 × ROE) + (0.2 × ROA) + (0.2 × NIM) - (0.2 × NPA) + (0.1 × CAR)
```
A higher score indicates better growth potential

#### 2. IT & Technology Sector

Key Ratios:
- Revenue Growth ≥ 12%
- Operating Margin ≥ 20%
- FCF Margin ≥ 15%
- ROE ≥ 20%
- P/E Ratio ≤ 30
- EV/EBITDA ≤ 15

Growth Score Formula:
```
Growth Score = (0.25 × Revenue Growth) + (0.25 × Operating Margin) + 
               (0.25 × FCF Margin) + (0.25 × ROE)
```

#### 3. FMCG & Consumer Goods Sector

Key Ratios:
- Revenue Growth ≥ 8%
- Gross Margin ≥ 50%
- ROE ≥ 18%
- Debt-to-Equity ≤ 0.5
- Dividend Yield ≥ 1.5%
- P/E Ratio ≤ 40

Growth Score Formula:
```
Growth Score = (0.25 × Revenue Growth) + (0.15 × Gross Margin) + 
               (0.2 × ROE) - (0.2 × D/E) + (0.05 × Dividend Yield)
```

#### 4. Automobiles Sector

Key Ratios:
- Revenue Growth ≥ 10%
- Operating Margin ≥ 12%
- Debt-to-Equity ≤ 1
- ROE ≥ 15%
- P/FCF ≤ 20

Growth Score Formula:
```
Growth Score = (0.3 × Operating Margin) + (0.25 × ROE) - 
               (0.2 × D/E) + (0.25 × Revenue Growth)
```

#### 5. Energy, Oil & Gas Sector

Key Ratios:
- EBITDA Margin ≥ 25%
- Debt-to-Equity ≤ 1.2
- Interest Coverage Ratio ≥ 4
- P/FCF ≤ 15
- Dividend Yield ≥ 3%

Growth Score Formula:
```
Growth Score = (0.3 × EBITDA Margin) - (0.2 × D/E) + 
               (0.3 × Interest Coverage) + (0.2 × Dividend Yield)
```

#### 6. Healthcare & Pharmaceuticals Sector

Key Ratios:
- Revenue Growth ≥ 10%
- Operating Margin ≥ 18%
- ROE ≥ 16%
- R&D Expenditure ≥ 5% of Revenue
- P/E Ratio ≤ 35

Growth Score Formula:
```
Growth Score = (0.25 × Revenue Growth) + (0.2 × Operating Margin) + 
               (0.2 × ROE) + (0.2 × EBITDA Growth) + 
               (0.15 × Free Cash Flow Growth)
```

#### 7. Retail Sector

Key Ratios:
- Inventory Turnover Ratio
- Operating Margin
- Revenue Growth
- Debt-to-Equity (D/E)
- Return on Equity (ROE)

Growth Score Formula:
```
Growth Score = (0.3 × Revenue Growth) + (0.2 × Operating Margin) + 
               (0.15 × ROE) - (0.15 × D/E) + 
               (0.2 × Free Cash Flow Growth)
```
## Features
- Proprietary sector-specific growth scoring
- AI-powered financial insights
- Comprehensive multi-sector analysis
- Research-backed analytical approach
- We have used web scrapping to get real time data which makes our model more accurate. 

## Prerequisites
- Python 3.8+
- Ollama
- Python libraries:
  - `ollama`
  - `json`

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/financial-insights-analyzer.git
cd financial-insights-analyzer
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Ollama
Follow the official Ollama installation guide:
- [Ollama Official Website](https://ollama.com/download)

### 4. Pull Required Model
```bash
ollama pull deepseek-r1:14b  # Default model used in the script
```

## Usage

### Running the Financial Analysis Tool
```bash
python app.py(or python model.py)
```

## Supported Sectors
- Banks and NBFC
- IT & Technology
- FMCG & Consumer Goods
- Automobiles
- Energy, Oil & Gas
- Healthcare & Pharmaceuticals
- Retail Sector

## Research Methodology
Our growth formulas are developed through:
- Comprehensive financial literature review
- Analysis of sector-specific performance indicators
- Weighted metric evaluation
- Continuous refinement based on market trends

## Customization
- Modify sector benchmarks
- Adjust growth formula weights
- Integrate new financial metrics

## Open Source License

### MIT License

Copyright (c) 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Disclaimer
This tool provides informational insights based on research and should not be considered definitive financial advice. Always consult with a financial professional before making investment decisions.

## Contributing
1. Fork the repository
2. Create your feature branch
3. Implement and document your research-based improvements
4. Submit a Pull Request

## Contact
Team No AI-021
