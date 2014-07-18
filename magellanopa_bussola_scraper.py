import sys, bs4, csv, urllib2

codici = {
	"200": "[livello Homepage] Amministrazione Trasparente",
	"235": "[livello 1] Attivit&#224; e procedimenti",
	"223": "[livello 1] Bandi di concorso",
	"244": "[livello 1] Bandi di gara e contratti",
	"252": "[livello 1] Beni immobili e gestione patrimonio",
	"249": "[livello 1] Bilanci",
	"211": "[livello 1] Consulenti e Collaboratori",
	"255": "[livello 1] Controlli e rilievi sull&#39;amministrazione",
	"243": "[livello 1] Controlli sulle imprese",
	"201": "[livello 1] Disposizioni generali",
	"230": "[livello 1] Enti Controllati",
	"266": "[livello 1] Informazioni Ambientali",
	"268": "[livello 1] Interventi straordinari e di emergenza",
	"264": "[livello 1] Opere Pubbliche",
	"205": "[livello 1] Organizzazione",
	"261": "[livello 1] Pagamenti dell&#39;amministrazione",
	"224": "[livello 1] Performance",
	"212": "[livello 1] Personale",
	"265": "[livello 1] Pianificazione e governo del territorio",
	"240": "[livello 1] Provvedimenti",
	"256": "[livello 1] Servizi Erogati",
	"245": "[livello 1] Sovvenzioni, contributi, sussidi, vantaggi economici",
	"267": "[livello 1] Strutture sanitarie private accreditate",
	"227": "[livello 2] Ammontare complessivo dei premi",
	"209": "[livello 2] Articolazione degli uffici",
	"247": "[livello 2] Atti di concessione",
	"203": "[livello 2] Atti Generali",
	"229": "[livello 2] Benessere organizzativo",
	"250": "[livello 2] Bilancio preventivo e consuntivo",
	"254": "[livello 2] Canoni di locazione o affitto",
	"257": "[livello 2] Carta dei servizi e standard di qualit&#224;",
	"220": "[livello 2] Contrattazione collettiva",
	"221": "[livello 2] Contrattazione integrativa",
	"258": "[livello 2] Costi contabilizzati",
	"246": "[livello 2] Criteri e modalit&#224;",
	"236": "[livello 2] Dati aggregati attivit&#224; amministrativa",
	"228": "[livello 2] Dati relativi ai premi",
	"239": "[livello 2] Dichiarazioni sostitutive e acquisizione d'ufficio dei dati",
	"214": "[livello 2] Dirigenti",
	"216": "[livello 2] Dotazione organica",
	"233": "[livello 2] Enti di diritto privato controllati",
	"231": "[livello 2] Enti pubblici vigilati",
	"263": "[livello 2] IBAN e pagamenti informatici",
	"213": "[livello 2] Incarichi amministrativi di vertice",
	"219": "[livello 2] Incarichi conferiti e autorizzati ai dipendenti",
	"262": "[livello 2] Indicatore di tempestivit&#224; dei pagamenti",
	"260": "[livello 2] Liste di attesa",
	"238": "[livello 2] Monitoraggio tempi procedimentali",
	"222": "[livello 2] OIV",
	"204": "[livello 2] Oneri informativi per cittadini e imprese",
	"206": "[livello 2] Organi di indirizzo politico-amministrativo",
	"271": "[livello 2] Organismo di Valutazione",
	"253": "[livello 2] Patrimonio immobiliare",
	"217": "[livello 2] Personale non a tempo indeterminato",
	"251": "[livello 2] Piano degli indicatori e risultati attesi di bilancio",
	"225": "[livello 2] Piano della Performance",
	"215": "[livello 2] Posizioni organizzative",
	"202": "[livello 2] Programma per la trasparenza e l&#39;integrit&#224;",
	"242": "[livello 2] Provvedimenti dirigenti",
	"241": "[livello 2] Provvedimenti organi indirizzo-politico",
	"234": "[livello 2] Rappresentazione grafica",
	"226": "[livello 2] Relazione sulla Performance",
	"208": "[livello 2] Rendiconti gruppi consiliari regionali/provinciali",
	"207": "[livello 2] Sanzioni per mancata comunicazione dei dati",
	"272": "[livello 2] Sistema di misurazione e valutazione della dirigenza",
	"232": "[livello 2] Societ&#224; partecipate",
	"218": "[livello 2] Tassi di assenza",
	"210": "[livello 2] Telefono e posta elettronica",
	"259": "[livello 2] Tempi medi di erogazione dei servizi",
	"237": "[livello 2] Tipologie di procedimento",
	"270": "[livello 3] Scadenzario dei nuovi obblighi amministrativi"
}

url_1 = "http://magellanopa.it/bussola/page.aspx?s=servizi-online&qs=yTOwTbr/QsJN46D|dB1zcQ==&ind="
url_2 = "&regn=TOTALE"

for c in codici.keys():
	url = url_1 + c + url_2
	outfile_name = codici[c].split('] ')[1].replace(' ', '_').replace('&#224;', 'a').replace('&#39;', '_').replace(',', '').replace('-', '_').replace('/', '_').replace('\'', '_') + '.tsv'
	print url, '--->', outfile_name

	soup = bs4.BeautifulSoup(urllib2.urlopen(url).read())
	
	div = [t for t in soup.findAll('div') if t.get('id') != None and t['id'].startswith("ctl00_ctl00_ContentPlaceHolderAreaOperativa_ContentPlaceHolderAreaOperativa_ctl00_ctl00_rptResult_")]
	
	with open(outfile_name, 'w') as outfile:
		csvwriter = csv.writer(outfile, delimiter='\t')
		csvwriter.writerow(['Amministrazione', 'Link', 'Tipo'])
	
		for d in div:
			tipo = d.find('h2').text.strip().split('Riepilogo Amministrazioni di tipo: ')[1]
			table = d.find('table')
			trs = table.findAll('tr')
			
			for row in trs[1:]:
				tds = row.findAll('td')
				csvwriter.writerow([tds[0].text.strip().encode('utf8'), tds[1].find('a')['href'].encode('utf8'), tipo.encode('utf8')])
	
