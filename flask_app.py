from flask import Flask, render_template, request
app = Flask(__name__)

from watson_developer_cloud import PersonalityInsightsV3

def ibm_watson_data(text):
    # change with your own credentials
    url = 'your-ibm-watson-perosnality-insights-url'
    apikey = 'your-ibm-watson-perosnality-insights-apikey'

    service = PersonalityInsightsV3(url=url , iam_apikey=apikey , version='2017-10-13' )
    data = service.profile(text, content_type='text/plain').get_result()
    result_needs = {need['name']:need['percentile'] for need in data['needs']}
    result_values = create_trait_plots(data['values'])
    result_personality = [create_trait_plots(big5['children']) for big5 in data['personality']]
    return result_needs, result_values, result_personality

def create_trait_plots(traits):
    result = {trait['name']: trait['percentile'] for trait in traits}
    return result

color = ['#003f5c', '#2f4b7c', '#665191', '#a05195', '#d45087', '#f95d6a', '#ff7c43', '#ffa600', '#003f5c', '#2f4b7c', '#665191', '#a05195', '#d45087', '#f95d6a', '#ff7c43', '#ffa600']

@app.route('/')
def main():
   return render_template('main.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      text = request.form['Text']
      result_needs, result_values, result_personality = ibm_watson_data(text)
      return render_template(
          "result.html",
          result_needs = result_needs, 
          result_values = result_values,
          result_personality = enumerate(result_personality),
          color=color,
        )

if __name__ == '__main__':
   app.run()


