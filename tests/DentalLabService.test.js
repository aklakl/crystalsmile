const { DentalLabService } = require('../src/models');

describe('DentalLabService', () => {
  describe('constructor', () => {
    test('creates instance with default values', () => {
      const service = new DentalLabService();
      
      expect(service.name).toBe('');
      expect(service.category).toBe('');
      expect(service.description).toBe('');
      expect(service.source).toBe('');
      expect(service.keywords).toEqual([]);
      expect(service.metadata).toEqual({});
      expect(service.crawledAt).toBeDefined();
    });

    test('creates instance with provided data', () => {
      const data = {
        name: 'Dental Crown',
        category: 'crowns',
        description: 'High-quality dental crowns',
        source: 'https://example.com',
        keywords: ['crown', 'dental'],
        metadata: { type: 'zirconia' }
      };

      const service = new DentalLabService(data);
      
      expect(service.name).toBe('Dental Crown');
      expect(service.category).toBe('crowns');
      expect(service.description).toBe('High-quality dental crowns');
      expect(service.source).toBe('https://example.com');
      expect(service.keywords).toEqual(['crown', 'dental']);
      expect(service.metadata).toEqual({ type: 'zirconia' });
    });
  });

  describe('isValid', () => {
    test('returns true for valid service with name', () => {
      const service = new DentalLabService({ name: 'Test Service' });
      expect(service.isValid()).toBe(true);
    });

    test('returns false for service without name', () => {
      const service = new DentalLabService();
      expect(service.isValid()).toBe(false);
    });

    test('returns false for service with empty name', () => {
      const service = new DentalLabService({ name: '' });
      expect(service.isValid()).toBe(false);
    });
  });

  describe('toJSON', () => {
    test('converts service to plain object', () => {
      const service = new DentalLabService({
        name: 'Test',
        category: 'crowns',
        description: 'Description',
        source: 'https://test.com',
        keywords: ['test'],
        metadata: { key: 'value' }
      });

      const json = service.toJSON();
      
      expect(json).toHaveProperty('name', 'Test');
      expect(json).toHaveProperty('category', 'crowns');
      expect(json).toHaveProperty('description', 'Description');
      expect(json).toHaveProperty('source', 'https://test.com');
      expect(json).toHaveProperty('keywords', ['test']);
      expect(json).toHaveProperty('metadata', { key: 'value' });
      expect(json).toHaveProperty('crawledAt');
    });
  });

  describe('fromJSON', () => {
    test('creates instance from plain object', () => {
      const obj = {
        name: 'From JSON',
        category: 'dentures'
      };

      const service = DentalLabService.fromJSON(obj);
      
      expect(service).toBeInstanceOf(DentalLabService);
      expect(service.name).toBe('From JSON');
      expect(service.category).toBe('dentures');
    });
  });
});
