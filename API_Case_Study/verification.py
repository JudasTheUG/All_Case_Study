import logging
from Utilities.LogUtil import Logger

log = Logger(__name__, logging.INFO)

def success_check(response):

    if response.status_code == 200:
        log.logger.info("\nTest Status : " + "Success")
        log.logger.info("Status Code : " + str(response.status_code))
        log.logger.info("Response Time : " + str(response.elapsed.total_seconds()))
        log.logger.info("Response URL : " + response.url)
        log.logger.info("Response Body : " + str(response))
    else:
        log.logger.info("\nTest Status : " + "Failed")
        log.logger.info("Status Code : " + str(response.status_code))
        log.logger.info("Response URL : " + response.url)
        log.logger.info("Response Body : " + str(response))


def not_found_check(response):
    if response.status_code == 404:
        log.logger.info("\nTest Status : " + "Success")
        log.logger.info("Status Code : " + str(response.status_code))
        log.logger.info("Response Time : " + str(response.elapsed.total_seconds()))
        log.logger.info("Response URL : " + response.url)
        log.logger.info("Response Body : " + str(response))
    else:
        log.logger.info("\nTest Status : " + "Failed")
        log.logger.info("Status Code : " + str(response.status_code))
        log.logger.info("Response URL : " + response.url)
        log.logger.info("Response Body : " + str(response))


def server_error_check(response):
    if response.status_code == 500:
        log.logger.info("\nTest Status : " + "Success")
        log.logger.info("Status Code : " + str(response.status_code))
        log.logger.info("Response Time : " + str(response.elapsed.total_seconds()))
        log.logger.info("Response URL : " + response.url)
        log.logger.info("Response Body : " + str(response))
    else:
        log.logger.info("\nTest Status : " + "Failed")
        log.logger.info("Status Code : " + str(response.status_code))
        log.logger.info("Response URL : " + response.url)
        log.logger.info("Response Body : " + str(response))


def bad_request_check(response):
    if response.status_code == 400:
        log.logger.info("\nTest Status : " + "Success")
        log.logger.info("Status Code : " + str(response.status_code))
        log.logger.info("Response Time : " + str(response.elapsed.total_seconds()))
        log.logger.info("Response URL : " + response.url)
        log.logger.info("Response Body : " + str(response))
    else:
        log.logger.info("\nTest Status : " + "Failed")
        log.logger.info("Status Code : " + str(response.status_code))
        log.logger.info("Response URL : " + response.url)
        log.logger.info("Response Body : " + str(response))