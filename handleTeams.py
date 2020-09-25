import time

from common.session import session
from common.ui_utils import ui_utils
from selenium.webdriver.common.by import By
from pprint import pprint
import sys, traceback
import json


# TODO instead of repeating using
# ```for i in range(self.defaultRepeat):```
# there is a package that can deal with this using methods and annotations for retry

class handleTeams(session):
    ui = None

    ses = None

    def getSessionAndLogin(self):
        pass

    defaultSleep = 1
    defaultRepeat = 3
    defaultWait = 10

    # Dev note:
    # it was working until it was not.. there were some issues with lags and not working links, etcp.
    def findAndClick(self, xpath):
        self.logger.info("findAndClick xpath: " + xpath)
        ui = self.ui
        ui.waitForElementOnPage(By.XPATH, xpath, self.defaultWait)
        time.sleep(self.defaultSleep)
        self.logger.info("findAndClick waited long enough")

        # this comment below is just for testing
        # for i in range(10):
        #     while True:
        #         try:
        #             el = self.find_element_by_xpath(xpath)
        #             el.click()
        #         except:
        #             time.sleep(self.defaultSleep)
        #             continue
        #         else:
        #             break
        el = self.find_element_by_xpath(xpath)
        el.click()
        self.logger.info("findAndClick clicked")
        # time.sleep(0.5)
        # time.sleep(self.defaultSleep)
        return el

    def updateTeams(self):
        current_milli_time = lambda: int(round(time.time() * 1000))

        self.logger.info("handleTeams.updateTeams")

        self.ui = ui_utils(self)
        ui = self.ui

        time_all_st = current_milli_time()
        self.logger.info("time_all_st: " + str(time_all_st))

        teamCnt = 0
        jsonFilePath = self.BASE_PATH + self.JSON_FILE_PATH
        self.logger.info("jsonFilePath: " + jsonFilePath)
        with open(jsonFilePath) as json_file:
            data = json.load(json_file)
            if (self.JSON_REC_REVERSE == "True"):
                data = reversed(data)
            if (self.JSON_REC_ALL != "True"):
                self.logger.info(
                    "Skipping some records, exec only for FROM: " + self.JSON_REC_FROM + " TO: " + self.JSON_REC_TO)

            for dSet in data:
                teamCnt = teamCnt + 1
                if (self.JSON_REC_ALL != "True"):
                    # I am too lazy to deal with error of ```data=data[self.JSON_REC_FROM:self.JSON_REC_TO]```
                    if (teamCnt < int(self.JSON_REC_FROM) or teamCnt > int(self.JSON_REC_TO)):
                        continue
                        # data = data[self.JSON_REC_FROM:self.JSON_REC_TO]

                self.logger.info(dSet.keys())
                link = list(dSet.keys())
                self.logger.info(link[0])

                time_team_st = current_milli_time()
                self.logger.info("time_team_st " + str(teamCnt) + ": " + str(time_team_st))
                try:
                    for i in range(self.defaultRepeat):
                        try:
                            # while True:g
                            self.logger.info("updateTeam-all-repeating: " + str(i))
                            self.updateMeeting((link[0]), dSet[link[0]])
                            time.sleep(self.defaultSleep)
                        except:
                            self.logger.info("updateTeam-all-repeating-exception " + str(i))
                        else:
                            break
                except:
                    self.logger.error("Smth went wrong with " + str(teamCnt) + " ")
                    self.logger.info(link[0])
                    self.logger.info(dSet[link[0]])
                    self.logger.info("Exception caught:")
                    self.logger.info('-' * 60)
                    # traceback.print_exc(file=sys.stdout)
                    # traceback.print_exc(file=self.logger. sys.stdout)
                    self.logger.error("Logging an exception " + str(traceback.format_exc()))
                    self.logger.info('-' * 60)
                    try:
                        self.web_driver.switch_to_window(self.web_driver.window_handles[1])
                        try:
                            self.web_driver.close()
                            self.web_driver.switch_to_window(self.web_driver.window_handles[0])
                        except:
                            self.logger.error("unable to close->selectFirstTab")
                        time.sleep(self.defaultSleep)
                    except:
                        self.logger.error("unable to selectSecondsTab->close->selectFirstTab")

                time_team_end = current_milli_time()
                self.logger.info("time_team_end " + str(teamCnt) + ": " + str(time_team_end))
                self.logger.info("time_team_diff " + str(teamCnt) + ": " + str(time_team_end - time_team_st))
                self.logger.info("time_start_diff " + str(teamCnt) + ": " + str(time_team_end - time_all_st))

        time_all_end = current_milli_time()
        self.logger.info("time_all_end: " + str(time_all_end))
        self.logger.info("time_all_diff: " + str(time_all_end - time_all_st))

    def updateMeeting(self, link, people):
        self.web_driver.get(link)

        time.sleep(self.defaultSleep)
        self.findAndClick("//*[@data-tid='joinOnWeb']")
        # time.sleep(self.defaultSleep)

        for i in range(self.defaultRepeat):
            # while True:
            self.logger.info("updateTeam-repeating: " + str(i))
            try:
                time.sleep(self.defaultSleep)
                self.findAndClick("//button[contains(@class,'join-btn')]")

                # from selenium.webdriver.common.action_chains import ActionChains
                # element_to_hover_over = firefox.find_element_by_id("baz")
                # element_to_hover_over = self.find_element_by_xpath("//button[contains(@class,'ts-calling-myself-video')]")
                # hover = ActionChains(self.web_driver).move_to_element(element_to_hover_over)
                # hover.perform()
                # TODO here is a problem that hover may be lost and so next click will not work ..
                # this is (hopefully) dealt with in exception block and repeat of surrounding try
                time.sleep(self.defaultSleep)
                self.findAndClick("//button[@id='roster-button']")
            except:  # Replace Exception with something more specific.
                self.web_driver.get(self.web_driver.current_url)
                time.sleep(self.defaultSleep)
                continue
            else:
                break

        time.sleep(self.defaultSleep)
        self.findAndClick("//button[@title='More options']")

        self.findAndClick("//a[@title='Manage permissions']")
        time.sleep(0.5)

        self.web_driver.switch_to_window(self.web_driver.window_handles[1])
        time.sleep(self.defaultSleep)

        self.findAndClick("//button[@id='dropdown-trigger-button-3']")

        self.findAndClick("//button[@id='dropdown-trigger-button-3']/../../ul/li[3]")

        for participantName in people:

            for i in range(5):
                # while True:
                self.logger.info("updateTeam-participant-picking-repeating : " + str(i))
                try:
                    self.logger.info("participantName " + participantName)
                    in_p = self.find_element_by_xpath("//input[@id='downshift-2-input']")
                    in_p.send_keys("(" + participantName + ")")
                    time.sleep(0.5)
                    try:
                        self.logger.info("people-picker-search open and click")
                        self.findAndClick("//div[@data-tid='people-picker-search']/div/ul/li[1]")
                    except:
                        self.logger.info("Smth went wrong with participant [" + participantName + "] at (" + link + ")")
                    time.sleep(0.2)
                    from selenium.webdriver.common.keys import Keys
                    in_p = self.find_element_by_xpath("//input[@id='downshift-2-input']")
                    in_p.send_keys(Keys.CONTROL + "a")
                    in_p.send_keys(Keys.DELETE)
                    time.sleep(0.2)
                    in_p.clear()
                except:  # Replace Exception with something more specific.
                    continue
                else:
                    break
        for i in range(self.defaultRepeat):
            # while True:
            self.logger.info("updateTeam-save-repeating : " + str(i))
            try:
                self.findAndClick("//button[@data-tid='Save button']")
                time.sleep(self.defaultSleep)
            except:  # Replace Exception with something more specific.
                continue
            else:
                break

        self.web_driver.close()

        self.web_driver.switch_to_window(self.web_driver.window_handles[0])
        time.sleep(self.defaultSleep)

        pass
