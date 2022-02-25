<drac2>
# get card data from variables
var='deck_of_illusions'
gv=get_svar(var,'3c73c64e-9975-4e9a-8dd0-6a7025e2122c')
cards=load_json(get_gvar(gv))
cards["Joker"]["img"]=image

arg="""&*&"""

# if the reset argument is given or there is no deck, a new deck is constructed from the gvar cards
new = ''
reset_cmd='reset'
if reset_cmd in arg or not (deck:=get(var)):
	arg = arg.replace(reset_cmd,'')
	deck=[]
	new='new '
	for c,d in cards.items():
		deck+=[c] * d.get('count',1)
else:
	if not (deck:= load_json(deck)):
		return f'echo You have no more cards left. You can reset with `{ctx.prefix}{ctx.alias} reset`'

# discard cards
pargs=argparse(arg)
if discards:=pargs.get('discard',pargs.get('d')):
	dis_carded = []
	for discard in discards:
		if discard.replace(" ","").isalpha():
			dis_cards=[card for card in deck if discard.lower() in card.lower() or discard.lower() in cards[card].name.lower()]
			deck=[card for card in deck if card not in dis_cards]
			dis_carded+=dis_cards
		elif amount:=roll(discard):
			for _ in range(amount):
				if not deck:
					break
				card=randchoice(deck)
				dis_carded.append(card)
				deck.remove(card)

	# persist
	character().set_cvar(var, dump_json(deck))
	# format output, can't draw a card as well
	desc='\n'.join(f':black_small_square: {card} - {cards[card].name}' for card in dis_carded)
	remaining = len(deck) or 'None'
	return f'''embed -title "{name} discards {len(dis_carded)} cards from {get('their','their')} {new}Deck of Illusions" -desc "{desc}" -f "Remaining|{remaining}"'''

arg=arg.strip('''"'“”''')

if arg:
	if select:={c:f for c,f in cards.items() if arg.lower() in c.lower() or arg.lower() in f.name.lower()}:
		for card, face in select.items():
			if card in deck:
				break
		else:
			return f'echo No more `{arg}` card.'
	else:
		return f'echo Unknown card : `{arg}`'
else:
	card = randchoice(deck)
	face = [d for c,d in cards.items() if c==card][0]

# update and persist the deck
deck.remove(card)
character().set_cvar(var, dump_json(deck))

# output
img_arg=f"-image {img}" if (img:=face.get('img')) else ""
illusion_size=face.get('size','')
remaining=len(deck) or 'None'
explain='''An illusion of one or more creatures forms over the thrown card and remains until dispelled. An illusory creature appears real, of the appropriate size, and behaves as if it were a real creature except that it can do no harm. 

While you are within 120 feet of the illusory creature and can see it, you can use an action to move it magically anywhere within 30 feet of its card. 

Any physical interaction with the illusory creature reveals it to be an illusion, because objects pass through it. Someone who uses an action to visually inspect the creature identifies it as illusory with a successful DC 15 Intelligence (Investigation) check. The creature then appears translucent.

The illusion lasts until its card is moved or the illusion is dispelled. When the illusion ends, the image on its card disappears, and that card can't be used again.'''

return f'''embed -title "{name} draws the {card} from {get('their','their')} {new}Deck of Illusions" -desc "*A {illusion_size} {face.name} appears within 30ft.*\n\n{explain}" {img_arg} -f "Cards remaining|{remaining}" '''
</drac2>
