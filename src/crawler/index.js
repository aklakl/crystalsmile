const DentalLabCrawler = require('./DentalLabCrawler');

module.exports = {
  DentalLabCrawler
};

// Allow direct execution
if (require.main === module) {
  const _crawler = new DentalLabCrawler();

  console.log('Dental Lab Services Crawler');
  console.log('===========================');
  console.log('');
  console.log('Usage: node src/crawler/index.js');
  console.log('');
  console.log('This crawler is designed to collect dental lab service information');
  console.log('from websites for marketing purposes.');
  console.log('');
  console.log('Available service categories:', require('../config').serviceCategories.join(', '));
  console.log('');
  console.log('Example usage in code:');
  console.log('  const { DentalLabCrawler } = require(\'./src/crawler\');');
  console.log('  const crawler = new DentalLabCrawler();');
  console.log('  const services = await crawler.crawlUrl(\'https://example.com/services\');');
}
