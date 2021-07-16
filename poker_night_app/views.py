from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from log_reg_app.models import *
from datetime import datetime
# Create your views here.


def home(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        this_user = User.objects.get(id=request.session['user_id'])
        now = datetime.now(tz=None)
        print(now)
        current_open_events = Event.objects.filter(is_full=False).exclude(hosted_by=this_user).exclude(attendees= this_user).exclude(scheduled_for__lt=now).order_by("scheduled_for")
        print('####################')
        print(current_open_events.all())
        context = {
        'all_events' : current_open_events,
        'this_user': this_user,
        }
        # all_events = events that are not in the past, are not hosted by user in session, not full
        return render(request,'home.html',context)

def my_events(request,user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        this_user = User.objects.get(id=request.session['user_id'])
        now = datetime.now(tz=None)
        print(now)
        attending_events = Event.objects.filter(attendees= this_user).exclude(scheduled_for__lt=now).exclude(hosted_by=this_user).order_by("scheduled_for")
        hosting_events = Event.objects.filter(hosted_by=this_user).exclude(scheduled_for__lt=now).order_by("scheduled_for")
        print('####################')
        context = {
        'hosting_events' : hosting_events,
        'attending_events' : attending_events,
        'this_user': this_user,
        }
        # all_events = events that are not in the past, are not hosted by user in session, not full
        return render(request,'my_events.html',context)

def game_register(request, event_id, game_type):
    if 'user_id' in request.session:
        if request.method == 'POST':
            this_event = Event.objects.get(id=event_id)
            this_user = User.objects.get(id=request.session['user_id'])
            this_event.attendees.add(this_user)
            print(f'{this_user.first_name} has registered for {this_event.id}')
            if this_event.attendees.count() == this_event.max_players:
                this_event.is_full = True
                this_event.save()
                return redirect(f'/poker_night/{event_id}/{game_type}/view')
            else:
                return redirect(f'/poker_night/{event_id}/{game_type}/view')
        else:
            return redirect('/poker_night/home')
    else:
        return redirect('/')

def game_unregister(request, event_id):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        this_event = Event.objects.get(id=event_id)
        this_user = User.objects.get(id=request.session['user_id'])
        this_event.attendees.remove(this_user)
        return redirect(f'/poker_night/{this_user.id}/my_events')

def host(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        this_user = User.objects.get(id=request.session['user_id'])
        context = {
        'this_user': this_user,
        }
        return render(request, 'host_form.html', context)

def host_tournament(request, user_id):
    if 'user_id' in request.session:
        this_user = User.objects.get(id=request.session['user_id'])
        context = {
            'this_user': this_user,
        }
        return render(request, 'tournament_host_form.html' , context)
    else:
        return redirect('/')

def host_cash_game(request, user_id):
    if 'user_id' in request.session:
        this_user = User.objects.get(id=request.session['user_id'])
        context = {
            'this_user': this_user,
        }
        return render(request, 'cash_host_form.html' , context)
    else:
        return redirect('/')

def event_create(request, user_id, game_type):
    if request.method=='POST':
        if game_type == "tournament":
            errors = Event.objects.tournament_validator(request.POST)
        else:
            errors = Event.objects.cash_game_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/poker_night/{user_id}/host/{game_type}')
        else:
            this_user = User.objects.get(id=request.session['user_id'])
            this_event = Event.objects.create(
                street = request.POST['street'],
                street_two = request.POST['street2'],
                city = request.POST['city'],
                state = request.POST['state'],
                zip_code = request.POST['zip_code'],
                scheduled_for = request.POST['date'],
                max_players = request.POST['max_players'],
                notes = request.POST['desc'],
                hosted_by = this_user,
            )
            this_event.attendees.add(this_user)

            if game_type == 'tournament':
                this_tournament = Tournament.objects.create(
                    style = request.POST['style'],
                    buy_in = request.POST['buy_in'],
                    re_entries = request.POST['re_entries'],
                    levels = request.POST['levels'],
                    event = this_event,
                )
                return redirect(f'/poker_night/{this_event.id}/tournament/view')
            
            else:
                small_blind = request.POST['s_blind']
                big_blind = request.POST['b_blind']
                form_stakes = f"${small_blind}/${big_blind}"
                this_cash_game = Cash_game.objects.create(
                    stakes = form_stakes, 
                    min_buy = request.POST['min_buy'],
                    max_buy = request.POST['max_buy'],
                    event = this_event,
                )
                return redirect(f'/poker_night/{this_event.id}/cash_game/view')
    else:
        return redirect('/poker_night/home')

def edit_tournament(request, event_id):
    if 'user_id' in request.session:
        
        this_user = User.objects.get(id=request.session['user_id'])
        this_event = Event.objects.get(id=event_id)
        context = {
            'this_user': this_user,
            'this_event': this_event,
        }
        if this_user == this_event.hosted_by:
            return render(request, 'tournament_edit_form.html' , context)
        else:
            return redirect('/poker_night/home')
    else:
        return redirect('/')

def edit_cash_game(request, event_id):
    if 'user_id' in request.session:
        this_user = User.objects.get(id=request.session['user_id'])
        this_event = Event.objects.get(id=event_id)
        form_stakes = this_event.cash_game.stakes
        stakes_split = form_stakes.split("/")
        sb = str(stakes_split[0][1:])
        bb = str(stakes_split[1][1:])
        print(sb, bb)
        context = {
            'this_user': this_user,
            'this_event': this_event,
            'small_blind': sb,
            'big_blind': bb,
        }
        if this_user == this_event.hosted_by:
            return render(request, 'cash_edit_form.html' , context)
        else:
            return redirect('/poker_night/home')
    else:
        return redirect('/')

def event_update(request, event_id, game_type):
    if request.method=='POST':
        if game_type == "tournament":
            errors = Event.objects.tournament_validator(request.POST)
        else:
            errors = Event.objects.cash_game_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/poker_night/{user_id}/host/{game_type}')
        else:
            this_user = User.objects.get(id=request.session['user_id'])
            this_event = Event.objects.get(id=event_id) 
            this_event.street = request.POST['street']
            this_event.street_two = request.POST['street2']
            this_event.city = request.POST['city']
            this_event.state = request.POST['state']
            this_event.zip_code = request.POST['zip_code']
            this_event.scheduled_for = request.POST['date']
            this_event.max_players = request.POST['max_players']
            this_event.notes = request.POST['desc']
            this_event.save()

            if game_type == 'tournament':
                this_tournament = Tournament.objects.get(id=this_event.tournament.id)
                this_tournament.style = request.POST['style']
                this_tournament.buy_in = request.POST['buy_in']
                this_tournament.re_entries = request.POST['re_entries']
                this_tournament.levels = request.POST['levels']
                this_tournament.save()
                return redirect(f'/poker_night/{event_id}/tournament/view')
            
            else:
                small_blind = request.POST['s_blind']
                big_blind = request.POST['b_blind']
                form_stakes = f"${small_blind}/${big_blind}"
                game_id = this_event.cash_game.id
                print(game_id)
                this_cash_game = Cash_game.objects.get(id=game_id)
                this_cash_game.stakes = form_stakes 
                this_cash_game.min_buy = request.POST['min_buy']
                this_cash_game.max_buy = request.POST['max_buy']
                this_cash_game.save()
                return redirect(f'/poker_night/{event_id}/cash_game/view')
    else:
        return redirect('/poker_night/home')

def event_cancel(request, event_id):
    this_user = User.objects.get(id=request.session['user_id'])
    this_event = Event.objects.get(id=event_id)
    if this_user.id == this_event.hosted_by.id:
        if 'user_id' not in request.session:
            return redirect('/')
        else:
            this_event.delete()
            return redirect(f'/poker_night/{this_user.id}/my_events')
    else:
        return redirect(f'/poker_night/{this_user.id}/my_events')

def view(request, event_id, game_type):
    if 'user_id' in request.session:
        this_event= Event.objects.get(id=event_id)
        this_user= User.objects.get(id=request.session['user_id'])
        context= {
            'this_user': this_user,
            'this_event': this_event,
        }
        if game_type == 'tournament':
            return render(request, 'tournament_view.html', context)
        elif game_type == 'cash_game':
            return render(request, 'cash_game_view.html', context)
    else:
        return redirect('/')

def comment(request, event_id):
    if request.method=='POST' and 'user_id' in request.session:
        this_user = User.objects.get(id=request.session['user_id'])
        this_event = Event.objects.get(id=event_id)
        this_comment = Comment.objects.create(
            content = request.POST['content'],
            user = User.objects.get(id=request.POST['user_id']),
            parent_event = this_event,
        )
        return redirect(f'/poker_night/{event_id}/tournament/view')
    else:
        return redirect('/')
    
def reply(request, event_id):
    if request.method=='POST' and 'user_id' in request.session:
        this_user = User.objects.get(id=request.session['user_id'])
        this_event = Event.objects.get(id=event_id)
        this_comment = Comment.objects.get(id=request.POST['comment_id'])
        this_reply= Reply.objects.create(
            content = request.POST['content'],
            user = User.objects.get(id=request.POST['user_id']),
            parent_event = this_event,
            parent_comment = this_comment,
        )
        return redirect(f'/poker_night/{event_id}/tournament/view')
    else:
        return redirect('/')
