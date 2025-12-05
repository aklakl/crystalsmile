const axios = require('axios');
const cheerio = require('cheerio');
const config = require('../config');
const { DentalLabService } = require('../models');
const { extractKeywords, categorizeService, cleanText, isValidUrl } = require('../utils');

/**
 * Dental Lab Services Crawler
 * Crawls websites to collect dental lab service information for marketing purposes
 */
class DentalLabCrawler {
  /**
   * Creates a new crawler instance
   * @param {Object} options - Crawler options
   */
  constructor(options = {}) {
    this.options = {
      ...config.crawler,
      ...options
    };

    this.axiosInstance = axios.create({
      timeout: this.options.timeout,
      headers: {
        'User-Agent': this.options.userAgent
      }
    });

    this.services = [];
  }

  /**
   * Fetches HTML content from a URL
   * @param {string} url - URL to fetch
   * @returns {Promise<string|null>} HTML content or null on error
   */
  async fetchPage(url) {
    if (!isValidUrl(url)) {
      console.error(`Invalid URL: ${url}`);
      return null;
    }

    try {
      const response = await this.axiosInstance.get(url);
      return response.data;
    } catch (error) {
      console.error(`Error fetching ${url}: ${error.message}`);
      return null;
    }
  }

  /**
   * Parses HTML content to extract dental lab service information
   * @param {string} html - HTML content
   * @param {string} sourceUrl - Source URL
   * @returns {DentalLabService[]} Array of extracted services
   */
  parseServices(html, sourceUrl) {
    if (!html) {
      return [];
    }

    const $ = cheerio.load(html);
    const services = [];

    // Extract service information from common HTML patterns
    // Look for service-related elements
    const serviceSelectors = [
      '.service',
      '.service-item',
      '.dental-service',
      '[data-service]',
      'article',
      '.card'
    ];

    for (const selector of serviceSelectors) {
      $(selector).each((_, element) => {
        const $el = $(element);
        const name = cleanText($el.find('h1, h2, h3, h4, .title, .service-title').first().text());
        const description = cleanText($el.find('p, .description, .content').first().text());

        if (name) {
          const service = new DentalLabService({
            name,
            description,
            source: sourceUrl,
            category: categorizeService(name, description),
            keywords: extractKeywords(`${name} ${description}`),
            metadata: {
              extractedFrom: selector
            }
          });

          if (service.isValid()) {
            services.push(service);
          }
        }
      });
    }

    // Also try to extract from general page content
    const pageTitle = cleanText($('title').text());
    const pageDescription = cleanText($('meta[name="description"]').attr('content') || '');

    if (pageTitle && pageTitle.toLowerCase().includes('dental')) {
      const pageService = new DentalLabService({
        name: pageTitle,
        description: pageDescription,
        source: sourceUrl,
        category: categorizeService(pageTitle, pageDescription),
        keywords: extractKeywords(`${pageTitle} ${pageDescription}`),
        metadata: {
          extractedFrom: 'page-meta'
        }
      });

      if (pageService.isValid()) {
        services.push(pageService);
      }
    }

    return services;
  }

  /**
   * Crawls a single URL and extracts dental lab services
   * @param {string} url - URL to crawl
   * @returns {Promise<DentalLabService[]>} Extracted services
   */
  async crawlUrl(url) {
    console.log(`Crawling: ${url}`);
    const html = await this.fetchPage(url);
    const services = this.parseServices(html, url);
    this.services.push(...services);
    console.log(`Found ${services.length} services from ${url}`);
    return services;
  }

  /**
   * Crawls multiple URLs
   * @param {string[]} urls - URLs to crawl
   * @returns {Promise<DentalLabService[]>} All extracted services
   */
  async crawlUrls(urls) {
    const results = [];

    for (const url of urls) {
      const services = await this.crawlUrl(url);
      results.push(...services);

      // Respect rate limiting
      if (this.options.requestDelay > 0) {
        await this.delay(this.options.requestDelay);
      }
    }

    return results;
  }

  /**
   * Delays execution
   * @param {number} ms - Milliseconds to delay
   * @returns {Promise<void>}
   */
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Gets all collected services
   * @returns {DentalLabService[]} All services
   */
  getServices() {
    return this.services;
  }

  /**
   * Clears collected services
   */
  clearServices() {
    this.services = [];
  }

  /**
   * Exports services to JSON format
   * @returns {Object[]} Services as JSON objects
   */
  exportToJSON() {
    return this.services.map(service => service.toJSON());
  }
}

module.exports = DentalLabCrawler;
