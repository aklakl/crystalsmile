const config = require('../config');

/**
 * Extracts marketing keywords from text content
 * @param {string} text - Text content to analyze
 * @returns {string[]} Array of found marketing keywords
 */
function extractKeywords(text) {
  if (!text || typeof text !== 'string') {
    return [];
  }

  const lowerText = text.toLowerCase();
  const foundKeywords = [];

  for (const keyword of config.marketingKeywords) {
    if (lowerText.includes(keyword.toLowerCase())) {
      foundKeywords.push(keyword);
    }
  }

  return [...new Set(foundKeywords)];
}

/**
 * Categorizes a dental service based on its description and name
 * @param {string} name - Service name
 * @param {string} description - Service description
 * @returns {string} Category name
 */
function categorizeService(name, description) {
  const text = `${name} ${description}`.toLowerCase();

  for (const category of config.serviceCategories) {
    if (text.includes(category)) {
      return category;
    }
  }

  return 'general';
}

/**
 * Cleans and normalizes text content
 * @param {string} text - Text to clean
 * @returns {string} Cleaned text
 */
function cleanText(text) {
  if (!text || typeof text !== 'string') {
    return '';
  }

  return text
    .replace(/\s+/g, ' ')
    .replace(/\n+/g, ' ')
    .trim();
}

/**
 * Validates a URL
 * @param {string} url - URL to validate
 * @returns {boolean} True if valid
 */
function isValidUrl(url) {
  if (!url || typeof url !== 'string') {
    return false;
  }

  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
}

module.exports = {
  extractKeywords,
  categorizeService,
  cleanText,
  isValidUrl
};
