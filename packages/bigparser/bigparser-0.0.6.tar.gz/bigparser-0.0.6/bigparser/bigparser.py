import requests
import json

'''
BpData This class implements the methods needed to connect to BigParser's
API to authenticate and fetch the required data
@author Ajay Arjun
@version 1.0
'''


class bigparser:
    '''
    This method makes generic post calls
    @param endPointa
            Target URI
    @param headers
            Headers to be passed for the current request
    @param data
            Body of the post request
    @return String returns the response as JSON Object
    '''

    def __post(self, uri, headers, data):
        try:
            response = requests.post(uri, data=json.dumps(data), headers=headers)
            # print(response)
            response.raise_for_status()
            if response.status_code == 200:
                if len(response.text):
                    responseData = json.loads(response.text)
                else:
                    return "200"
                return responseData
        except requests.exceptions.HTTPError as err:
            print("Http Error")
            raise RuntimeError(err.response.text)
        except requests.exceptions.Timeout as err:
            print("TimeOut")
            raise RuntimeError(err.response.text)
        except requests.exceptions.ConnectionError as err:
            print("ConnectionError")
            raise RuntimeError(err.response.text)
        except requests.exceptions.RequestException as err:
            print("Error")
            raise RuntimeError(err.response.text)

    '''
    This method makes generic get calls
    @param endPoint 
            Target URI
    @param headers
            Headers to be passed for the current request
    @return String returns the response as JSON Object
    '''

    def __get(self, uri, headers):
        try:
            response = requests.get(uri, headers=headers)
            response.raise_for_status()
            if response.status_code == 200:
                responseData = json.loads(response.text)
                return responseData
        except requests.exceptions.HTTPError as err:
            print("Http Error")
            return err.response.text
        except requests.exceptions.Timeout as err:
            print("TimeOUt")
            return err.response.text
        except requests.exceptions.ConnectionError as err:
            print("ConnectionError")
            return err.response.text
        except requests.exceptions.RequestException as err:
            print("Error")
            return err.response.text

    '''
    This method performs the task of login into BigParser account and fetch authId for future calls
    @param emailId
        emailId/username of your account
    @param password
        password to login into BigParser account
    @return String returns the response as JSON Object
    '''

    @classmethod
    def login(self, username, password):
        uri = "https://www.bigparser.com/APIServices/api/common/login"
        data = {'emailId': '' + username + '', 'password': '' + password + ''}
        headers = {'content-type': 'application/json'}
        response = bigparser.__post(self, uri, headers, data)
        authId = response["authId"]
        return authId

    '''
    This method performs the task of login into BigParser account and fetch authId for future calls
    @param emailId
        emailId/username of your account
    @param password
        password to login into BigParser account
    @return String returns the response as JSON Object
    '''

    @classmethod
    def signup(self, emailId, password, fullName, mobileNumber, srcName=None, visitId=None):
        uri = "https://www.bigparser.com/APIServices/api/common/signup"
        data = dict()
        data['emailId'] = emailId
        data['fullName'] = fullName
        data['password'] = password
        data['mobileNumber'] = mobileNumber
        if srcName is not None:
            data['srcName'] = srcName
        if visitId is not None:
            data['visitId'] = visitId
        print(data)
        headers = {'content-type': 'application/json'}
        response = bigparser.post(self, uri, headers, data)
        if response == "200":
            return "Please confirm your email address by signing in to your email to complete registration"
        return response

    '''
    Fetches rows from the specified grid. Parameters to query the grid are passed as a part of the post request
    @param emailId
        emailId/username of your account
    @param password
        password to login into BigParser account
    @param gridId
        gridId of the required grid
    @return String returns the response as JSON in string format
    '''

    @classmethod
    def getHeader(self, authId, gridId):
        uri = "https://www.bigparser.com/APIServices/api/grid/headers?gridId=" + gridId
        headers = {'content-type': 'application/json', 'authId': '' + authId + ''}
        response = bigparser.__get(self, uri, headers)
        return response

    '''
    Fetches rows from the specified grid. Parameters to query the grid are passed as a part of the post request
    @param emailId
        emailId/username of your account
    @param password
        password to login into BigParser account
    @param data
        comprises the options to query the grid in the form of JSON object.
    @return String returns the response as JSON in string format
    '''

    @classmethod
    def getData(self, authId, gridId, rowCount=50, selectColumnsStoreName=None, tags=None,
                keywords=None, sortKeys=None):
        uri = "https://www.bigparser.com/APIServices/api/query/table"
        headers = {'content-type': 'application/json', 'authId': '' + authId + ''}
        data = dict()
        data['gridId'] = gridId
        data['rowCount'] = rowCount
        if selectColumnsStoreName is not None:
            data['selectColumnsStoreName'] = selectColumnsStoreName
        if tags is not None:
            data['tags'] = tags
        if keywords is not None:
            data['keywords'] = keywords
        if sortKeys is not None:
            data['sortKeys'] = sortKeys
        response = bigparser.__post(self, uri, headers, data)
        return response

    '''
    Fetches rows from the specified grid. Parameters to query the grid are passed as a part of the post request
    @param emailId
        emailId/username of your account
    @param password
        password to login into BigParser account
    @param data
        comprises the options to query the grid in the form of JSON object.
    @return String returns the response as JSON in string format
    '''

    @classmethod
    def searchColumn(self, authId, gridId, columnStoreName, searchKey, pageSize):
        uri = "https://www.bigparser.com/APIServices/api/query/search"
        headers = {'content-type': 'application/json', 'authId': '' + authId + ''}
        data = dict()
        data['gridId'] = gridId
        data['columnStoreName'] = columnStoreName
        data['searchKey'] = searchKey
        data['pageSize'] = pageSize
        response = bigparser.post(self, uri, headers, data)
        return response

    @classmethod
    def getLastRow(self, authId, gridId, rowCount=50, selectColumnsStoreName=None, tags=None,
                   keywords=None, sortFields=None):
        uri = "https://www.bigparser.com/APIServices/api/query/table"
        headers = {'content-type': 'application/json', 'authId': '' + authId + ''}
        data = dict()
        data['gridId'] = gridId
        data['rowCount'] = rowCount
        if selectColumnsStoreName is not None:
            data['selectColumnsStoreName'] = selectColumnsStoreName
        if tags is not None:
            data['tags'] = tags
        if keywords is not None:
            data['keywords'] = keywords
        if sortFields is not None:
            data['sortFields'] = sortFields
        response = bigparser.post(self, uri, headers, data)
        count = (response['count'])
        uri = bigparser.prod_uri + "api/query/table?startIndex=" + str(count) + "&endIndex=" + str(
            count)
        response = bigparser.post(self, uri, headers, data)
        print(response)

    @classmethod
    def isFileExists(self, authId, filename):
        uri = "https://www.bigparser.com/APIServices/api/upload/isFileExisting"
        headers = {'content-type': 'application/json', 'authId': '' + authId + ''}
        data = dict()
        data['filename'] = [filename]
        response = bigparser.post(self, uri, headers, data)
        print(response)
