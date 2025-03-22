import requests
from django.shortcuts import render

def convert_currency(request):
    if request.method == 'POST':
        try:
            amount = float(request.POST['amount'])
            from_currency = request.POST['from_currency']
            to_currency = request.POST['to_currency']
            
            url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            data = response.json()
            
            rate = data['rates'][to_currency]
            converted_amount = amount * rate
            
            return render(request, 'converter/result.html', {
                'amount': amount,
                'from_currency': from_currency,
                'to_currency': to_currency,
                'converted_amount': round(converted_amount, 2)
            })
        except (KeyError, ValueError) as e:
            return render(request, 'converter/convert.html', {
                'error': 'Invalid input or currency code.'
            })
        except requests.RequestException as e:
            return render(request, 'converter/convert.html', {
                'error': 'Error fetching exchange rates. Please try again later.'
            })
    
    return render(request, 'converter/convert.html')