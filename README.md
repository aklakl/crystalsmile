# CrystalSmile - Dental Lab Services Crawler

A Node.js crawler designed to collect and organize dental lab service information for marketing purposes.

## Features

- **Web Crawler**: Fetches and parses web pages to extract dental lab service information
- **Marketing Keywords**: Automatically extracts marketing-relevant keywords from content
- **Service Categorization**: Classifies services into categories (crowns, bridges, dentures, implants, etc.)
- **Data Models**: Structured data models for dental lab services
- **Rate Limiting**: Built-in request delay to respect website rate limits

## Installation

```bash
npm install
```

## Usage

### As a Module

```javascript
const { DentalLabCrawler, DentalLabService } = require('crystalsmile');

// Create a new crawler instance
const crawler = new DentalLabCrawler({
  requestDelay: 2000,  // 2 second delay between requests
  timeout: 30000       // 30 second timeout
});

// Crawl a single URL
const services = await crawler.crawlUrl('https://example-dental-lab.com/services');

// Export results as JSON
const jsonData = crawler.exportToJSON();
console.log(jsonData);
```

### Available Service Categories

- Crowns
- Bridges
- Dentures
- Implants
- Veneers
- Orthodontics
- Prosthodontics
- Restorations
- Cosmetic
- General

## API Reference

### DentalLabCrawler

The main crawler class for collecting dental lab services.

#### Constructor Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `maxConcurrent` | number | 5 | Maximum concurrent requests |
| `requestDelay` | number | 1000 | Delay between requests (ms) |
| `timeout` | number | 30000 | Request timeout (ms) |
| `userAgent` | string | 'CrystalSmile...' | User agent string |

#### Methods

- `crawlUrl(url)` - Crawl a single URL
- `crawlUrls(urls)` - Crawl multiple URLs
- `parseServices(html, sourceUrl)` - Parse HTML and extract services
- `getServices()` - Get all collected services
- `clearServices()` - Clear collected services
- `exportToJSON()` - Export services as JSON

### DentalLabService

Data model for dental lab services.

#### Properties

- `name` - Service name
- `category` - Service category
- `description` - Service description
- `source` - Source URL
- `keywords` - Marketing keywords
- `metadata` - Additional metadata
- `crawledAt` - Timestamp when service was crawled

## Testing

```bash
npm test
```

## License

Apache-2.0