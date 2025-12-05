const { DentalLabCrawler } = require('../src/crawler');
const { DentalLabService } = require('../src/models');

describe('DentalLabCrawler', () => {
  let crawler;

  beforeEach(() => {
    crawler = new DentalLabCrawler();
  });

  describe('constructor', () => {
    test('creates instance with default options', () => {
      expect(crawler.options).toBeDefined();
      expect(crawler.options.timeout).toBeDefined();
      expect(crawler.options.userAgent).toBeDefined();
    });

    test('allows custom options', () => {
      const customCrawler = new DentalLabCrawler({
        timeout: 5000,
        requestDelay: 500
      });
      
      expect(customCrawler.options.timeout).toBe(5000);
      expect(customCrawler.options.requestDelay).toBe(500);
    });
  });

  describe('parseServices', () => {
    test('extracts services from HTML with service elements', () => {
      const html = `
        <html>
          <head><title>Dental Lab Services</title></head>
          <body>
            <div class="service">
              <h2>Dental Crowns</h2>
              <p>High-quality zirconia crowns for dental restoration</p>
            </div>
            <div class="service">
              <h2>Dental Bridges</h2>
              <p>Custom bridges for missing teeth</p>
            </div>
          </body>
        </html>
      `;

      const services = crawler.parseServices(html, 'https://example.com');
      
      expect(services.length).toBeGreaterThan(0);
      expect(services[0]).toBeInstanceOf(DentalLabService);
    });

    test('extracts services from article elements', () => {
      const html = `
        <html>
          <body>
            <article>
              <h3>Implant Services</h3>
              <p>Dental implants and restorations</p>
            </article>
          </body>
        </html>
      `;

      const services = crawler.parseServices(html, 'https://example.com');
      
      expect(services.length).toBeGreaterThan(0);
    });

    test('returns empty array for empty HTML', () => {
      expect(crawler.parseServices(null, 'https://example.com')).toEqual([]);
      expect(crawler.parseServices('', 'https://example.com')).toEqual([]);
    });

    test('extracts page metadata when dental-related', () => {
      const html = `
        <html>
          <head>
            <title>Dental Lab - Premium Services</title>
            <meta name="description" content="Full-service dental laboratory">
          </head>
          <body></body>
        </html>
      `;

      const services = crawler.parseServices(html, 'https://example.com');
      
      expect(services.some(s => s.name.includes('Dental Lab'))).toBe(true);
    });
  });

  describe('getServices and clearServices', () => {
    test('stores and retrieves services', () => {
      const html = `
        <html>
          <body>
            <div class="service">
              <h2>Test Service</h2>
              <p>Description</p>
            </div>
          </body>
        </html>
      `;

      crawler.parseServices(html, 'https://example.com').forEach(s => {
        crawler.services.push(s);
      });

      expect(crawler.getServices().length).toBeGreaterThan(0);

      crawler.clearServices();
      expect(crawler.getServices().length).toBe(0);
    });
  });

  describe('exportToJSON', () => {
    test('exports services as JSON objects', () => {
      crawler.services.push(new DentalLabService({
        name: 'Test Service',
        category: 'crowns'
      }));

      const json = crawler.exportToJSON();
      
      expect(Array.isArray(json)).toBe(true);
      expect(json[0]).toHaveProperty('name', 'Test Service');
      expect(json[0]).toHaveProperty('category', 'crowns');
    });
  });

  describe('delay', () => {
    test('delays execution', async () => {
      const start = Date.now();
      await crawler.delay(100);
      const elapsed = Date.now() - start;
      
      expect(elapsed).toBeGreaterThanOrEqual(90);
    });
  });
});
