from forex_python.converter import CurrencyRates

def currency():
	c = CurrencyRates()
	usd = c.get_rate('USD','RON')
	eur = c.get_rate('EUR','RON')
	
	return {
		'USD': f'{usd:,.2f}',
		'EUR': f'{eur:,.2f}'
	}