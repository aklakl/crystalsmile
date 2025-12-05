/**
 * Configuration for the dental lab services crawler
 */
module.exports = {
  // Crawler settings
  crawler: {
    // Maximum concurrent requests
    maxConcurrent: 5,
    // Delay between requests in milliseconds
    requestDelay: 1000,
    // Request timeout in milliseconds
    timeout: 30000,
    // User agent for requests
    userAgent: 'CrystalSmile Dental Lab Services Crawler/1.0'
  },

  // Dental service categories for classification
  serviceCategories: [
    'crowns',
    'bridges',
    'dentures',
    'implants',
    'veneers',
    'orthodontics',
    'prosthodontics',
    'restorations',
    'cosmetic',
    'general'
  ],

  // Marketing keywords related to dental lab services
  marketingKeywords: [
    'dental lab',
    'dental laboratory',
    'dental prosthetics',
    'dental restoration',
    'dental implants',
    'dental crowns',
    'dental bridges',
    'full dentures',
    'partial dentures',
    'porcelain veneers',
    'zirconia crowns',
    'dental ceramics',
    'CAD/CAM dentistry',
    'digital dentistry',
    'custom dental work'
  ]
};
