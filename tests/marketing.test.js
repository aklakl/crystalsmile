const { extractKeywords, categorizeService, cleanText, isValidUrl } = require('../src/utils');

describe('Marketing Utils', () => {
  describe('extractKeywords', () => {
    test('extracts marketing keywords from text', () => {
      const text = 'We offer dental lab services including dental crowns and dental bridges';
      const keywords = extractKeywords(text);
      
      expect(keywords).toContain('dental crowns');
      expect(keywords).toContain('dental bridges');
    });

    test('returns empty array for empty text', () => {
      expect(extractKeywords('')).toEqual([]);
      expect(extractKeywords(null)).toEqual([]);
      expect(extractKeywords(undefined)).toEqual([]);
    });

    test('is case insensitive', () => {
      const text = 'DENTAL LAB and Dental Laboratory services';
      const keywords = extractKeywords(text);
      
      expect(keywords).toContain('dental lab');
      expect(keywords).toContain('dental laboratory');
    });

    test('returns unique keywords only', () => {
      const text = 'dental lab dental lab dental lab';
      const keywords = extractKeywords(text);
      
      expect(keywords.filter(k => k === 'dental lab').length).toBe(1);
    });
  });

  describe('categorizeService', () => {
    test('categorizes crown services', () => {
      expect(categorizeService('Zirconia Crowns', 'Premium crown services')).toBe('crowns');
    });

    test('categorizes denture services', () => {
      expect(categorizeService('Full Dentures', 'Complete denture solutions')).toBe('dentures');
    });

    test('categorizes implant services', () => {
      expect(categorizeService('Dental Implants', 'Implant restoration')).toBe('implants');
    });

    test('returns general for unmatched services', () => {
      expect(categorizeService('Custom Work', 'Specialized dental work')).toBe('general');
    });
  });

  describe('cleanText', () => {
    test('removes extra whitespace', () => {
      expect(cleanText('Hello    World')).toBe('Hello World');
    });

    test('removes newlines', () => {
      expect(cleanText('Hello\n\nWorld')).toBe('Hello World');
    });

    test('trims whitespace', () => {
      expect(cleanText('  Hello World  ')).toBe('Hello World');
    });

    test('handles empty input', () => {
      expect(cleanText('')).toBe('');
      expect(cleanText(null)).toBe('');
      expect(cleanText(undefined)).toBe('');
    });
  });

  describe('isValidUrl', () => {
    test('returns true for valid URLs', () => {
      expect(isValidUrl('https://example.com')).toBe(true);
      expect(isValidUrl('http://test.com/path')).toBe(true);
      expect(isValidUrl('https://sub.domain.com:8080/path?query=1')).toBe(true);
    });

    test('returns false for invalid URLs', () => {
      expect(isValidUrl('not-a-url')).toBe(false);
      expect(isValidUrl('')).toBe(false);
      expect(isValidUrl(null)).toBe(false);
      expect(isValidUrl(undefined)).toBe(false);
    });
  });
});
