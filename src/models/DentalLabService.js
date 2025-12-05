/**
 * Dental Lab Service Model
 * Represents a dental lab service with marketing-relevant information
 */
class DentalLabService {
  /**
   * Creates a new DentalLabService instance
   * @param {Object} data - Service data
   * @param {string} data.name - Service name
   * @param {string} data.category - Service category (e.g., 'crowns', 'dentures', 'implants')
   * @param {string} data.description - Service description
   * @param {string} data.source - Source URL where the service was found
   * @param {string[]} data.keywords - Marketing keywords
   * @param {Object} data.metadata - Additional metadata
   */
  constructor(data = {}) {
    this.name = data.name || '';
    this.category = data.category || '';
    this.description = data.description || '';
    this.source = data.source || '';
    this.keywords = data.keywords || [];
    this.metadata = data.metadata || {};
    this.crawledAt = data.crawledAt || new Date().toISOString();
  }

  /**
   * Validates the service data
   * @returns {boolean} True if valid
   */
  isValid() {
    return Boolean(this.name && this.name.length > 0);
  }

  /**
   * Converts the service to a plain object
   * @returns {Object} Plain object representation
   */
  toJSON() {
    return {
      name: this.name,
      category: this.category,
      description: this.description,
      source: this.source,
      keywords: this.keywords,
      metadata: this.metadata,
      crawledAt: this.crawledAt
    };
  }

  /**
   * Creates a DentalLabService from a plain object
   * @param {Object} obj - Plain object
   * @returns {DentalLabService} New instance
   */
  static fromJSON(obj) {
    return new DentalLabService(obj);
  }
}

module.exports = DentalLabService;
