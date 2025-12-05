const { DentalLabCrawler } = require('./crawler');
const { DentalLabService } = require('./models');
const config = require('./config');
const utils = require('./utils');

module.exports = {
  DentalLabCrawler,
  DentalLabService,
  config,
  utils
};
