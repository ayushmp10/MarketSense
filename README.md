# MarketSense 📈

A real-time financial news sentiment analyzer that helps investors gauge market sentiment for specific stock tickers. This web application fetches the latest news articles and analyzes their sentiment to provide insights into market perception.

## Features

- **Real-time News Fetching**: Retrieves the latest financial news articles for any stock ticker
- **Advanced Sentiment Analysis**: Analyzes news sentiment using both external libraries and custom financial-specific algorithms
- **Enhanced Relevance Filtering**: Ensures news articles are actually related to the searched stock ticker
- **Responsive Design**: Clean, modern interface built with Tailwind CSS
- **Detailed Results**: Shows individual article sentiments and overall market sentiment

## How It Works

1. **Enter a Stock Ticker**: Input any stock symbol (e.g., AAPL, TSLA, GOOGL)
2. **Fetch News**: The app searches for recent financial news related to the ticker
3. **Analyze Sentiment**: Each article's title and description are analyzed for sentiment
4. **View Results**: See overall sentiment and individual article breakdowns

## Sentiment Categories

- **Positive**: Strong positive sentiment (score > 0.5)
- **Slightly Positive**: Mild positive sentiment (0 < score ≤ 0.5)
- **Neutral**: No clear sentiment bias (score = 0)
- **Slightly Negative**: Mild negative sentiment (-0.5 ≤ score < 0)
- **Negative**: Strong negative sentiment (score < -0.5)

## Setup Instructions

### Prerequisites

- A web browser (Chrome, Firefox, Safari, etc.)
- Python 3.x (for running local server)
- NewsAPI key (free from [newsapi.org](https://newsapi.org/))

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ayushmp10/MarketSense.git
   cd MarketSense
   ```

2. **Get your NewsAPI key**:
   - Visit [newsapi.org](https://newsapi.org/)
   - Sign up for a free account
   - Copy your API key

3. **Configure the API key**:
   - Open `index.html` in a text editor
   - Find line 82: `const NEWS_API_KEY = '55318ea279864b8891f7545c161efd9c';`
   - Replace with your actual API key

4. **Start the local server**:
   ```bash
   python -m http.server 8000
   ```

5. **Open in browser**:
   - Navigate to `http://localhost:8000`
   - Start analyzing stock sentiment!

## Usage Examples

### Popular Stock Tickers to Try

- **Tech Giants**: AAPL, GOOGL, MSFT, AMZN, META
- **Electric Vehicles**: TSLA, RIVN, LCID
- **Banking**: JPM, BAC, WFC, GS
- **Healthcare**: JNJ, PFE, UNH, MRNA

### Sample Workflow

1. Enter "AAPL" in the search box
2. Click "Analyze Sentiment"
3. View the overall sentiment score
4. Scroll through individual articles with their sentiment ratings
5. Click article titles to read full stories

## Technical Details

### Architecture

- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Styling**: Tailwind CSS via CDN
- **Sentiment Analysis**: 
  - Primary: Sentiment.js library
  - Fallback: Custom financial-specific word analysis
- **News API**: NewsAPI.org for real-time news data

### Key Features

- **Robust Error Handling**: Graceful fallbacks and user-friendly error messages
- **Relevance Filtering**: Advanced search queries and post-processing filters
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Performance Optimized**: Efficient API calls and DOM manipulation

### Sentiment Analysis Algorithm

The application uses a two-tier approach:

1. **Primary**: External sentiment library (Sentiment.js)
2. **Fallback**: Custom algorithm with 80+ financial-specific positive/negative keywords

Financial keywords include:
- **Positive**: growth, profit, surge, bullish, upgrade, beat, etc.
- **Negative**: loss, decline, bearish, downgrade, miss, crash, etc.

## API Rate Limits

- **NewsAPI Free Tier**: 1,000 requests per month
- **Rate Limit**: 1 request per second
- **Historical Data**: Up to 1 month for free accounts

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Roadmap

- [ ] Add historical sentiment tracking
- [ ] Implement multiple news source integration
- [ ] Add sentiment trend visualization charts
- [ ] Include social media sentiment analysis
- [ ] Add portfolio-level sentiment analysis
- [ ] Implement real-time updates via WebSocket

## Troubleshooting

### Common Issues

**"No recent news found"**
- Try a more popular ticker symbol
- Check if the company name matches the ticker

**"Failed to fetch news"**
- Verify your NewsAPI key is correct
- Check your internet connection
- Ensure you haven't exceeded API rate limits

**"Sentiment is not a constructor"**
- The fallback sentiment analyzer will automatically engage
- This doesn't affect functionality

### Browser Compatibility

- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for educational and informational purposes only. It should not be used as the sole basis for investment decisions. Always conduct your own research and consult with financial advisors before making investment choices.

## Acknowledgments

- [NewsAPI](https://newsapi.org/) for providing news data
- [Sentiment.js](https://github.com/thisandagain/sentiment) for sentiment analysis
- [Tailwind CSS](https://tailwindcss.com/) for styling framework
- [Google Fonts](https://fonts.google.com/) for the Inter font family

---

**Built with ❤️ by [ayushmp10](https://github.com/ayushmp10)**

For questions or support, please open an issue on GitHub.
