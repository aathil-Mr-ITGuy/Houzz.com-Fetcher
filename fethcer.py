import requests
import pandas as pd

base_url = 'https://www.houzz.com/professionals/design-build/probr0-bo~t_11793?fi='
#7127
urls = [f"{base_url}{i}&spf=navigate" for i in range(0,15, 15 )]

header = {
    'x-hz-request' : 'true',
    'x-hz-spf-request' : 'true',
    'x-requested-with' : 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'Cookie': '_csrf=fttpn5lo56xNF2UtWVDrj3cU; jdv=t7WOzUb2vHLZtWVVHSg5XJMfN7ua9zR%2FUkXvYNQLX0PmhhdCy7%2F8KLbn6JqqGArpBOovdpz3Rwn7HxMmdWmy0Nr6uNgQ; prf=prodirDistFil%7C%7D; v=1703835625_05019397-c28b-47ab-8206-f631e03a050f_ba072119a987b2e9862292e9b065c91b'
    
}

def add_decimal_after_first_digit(number):
    # Convert the number to a string
    number_str = str(number)

    # Insert a period after the first character
    modified_number_str = number_str[0] + '.' + number_str[1:]

    # Convert the modified string back to a float
    modified_number = float(modified_number_str)

    return modified_number

def get_prof_details(proffesional_store,professinal_id):
    prof_details = {}
    try:
        
        print(f"professinal_id{professinal_id}")
        prof_data = proffesional_store['data'][str(professinal_id)]
        if len(prof_data):
            prof_details['location'] = prof_data['location']
            prof_details['city'] = prof_data['city']
            prof_details['state'] = prof_data['state']
            prof_details['zip'] = prof_data['zip']
            prof_details['country'] = prof_data['country']
            prof_details['numberof_reviews'] = prof_data['numReviews']
            try:
                numReviews = prof_data['reviewRating']
                numReviews = add_decimal_after_first_digit(numReviews)
                prof_details['rating'] = numReviews
            except:
                pass
            # prof_details['rating'] = prof_data['reviewRating']
            prof_details['featuredReview'] = prof_data['mostRecentReview']['body'].strip()
            prof_details['featuredReview_by'] = prof_data['mostRecentReview']['user']['displayName']
    except Exception as e:
        print(f"Error in getting prof data {e}")
        pass
    return prof_details

companies = []
for url in urls:
    print(f"url is {url}")
    
    response = requests.get(url, headers=header)
    if response.status_code == 200:
        

        try:
            res = response.json()['ctx']
            data = res['data']['stores']['data']
            user_stores = data ['UserStore']['data']
            proffesional_store = data ['ProfessionalStore']

            try:
                for key, values in user_stores.items():
                    store_detail = {}
                    # print(F"data_value {type(values)}")
                    try:
                        name = values['displayName']
                    except:
                        name = 'N/A'
                        pass

                    try:
                        professinal_id = values['userId']
                        professinal_data = get_prof_details(proffesional_store,professinal_id)
                        print(f"professinal_data {professinal_data}")
                    except:
                        professinal_id = 'N/A'
                        pass

                    store_detail['Name'] = name
                    store_detail['Professinal Id'] = professinal_id

                    if len(professinal_data):
                        res = store_detail | professinal_data
                        companies.append(res)
                    else :
                        companies.append(store_detail)
                    # print(f"name {name}")

                    # for identfier, data_value in values.items():


            except Exception as e:
                print(f"Error in getting stores {e}")
                pass

            # print(f"user_store is {type(user_stores)}")

            # print(f"proffesional_store is {proffesional_store}")

        except Exception as e:
            print(f"Error in getting data {e}")
            pass

        # data = res
        
        # print(f"Status is 200")
    else:
        print(f"Error in fetching results: {response.status_code}")

if len(companies):
    df = pd.DataFrame(companies)
    df.to_csv("All companies.csv", index=False)
