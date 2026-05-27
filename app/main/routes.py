from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from sqlalchemy import select
from app import db
from app.main import main
from app.main.forms import PromptEntryForm, AIDiaryEntryForm, PromptForm

from app.models import PromptEntry, Tag, AIDiaryEntry

@main.route('/')
@main.route('/index')
def index():
    q = request.args.get('q', '')
    tag_name = request.args.get('tag', '')
    
    stmt = select(PromptEntry)
    if q:
        stmt = stmt.where(
            PromptEntry.title.ilike(f'%{q}%') | 
            PromptEntry.original_prompt.ilike(f'%{q}%') |
            PromptEntry.negative_prompt.ilike(f'%{q}%')
        )
    if tag_name:
        tag = db.session.scalar(select(Tag).where(Tag.name == tag_name))
        if tag:
            stmt = stmt.where(PromptEntry.tags.contains(tag))
        else:
            stmt = stmt.where(db.false())
            
    stmt = stmt.order_by(PromptEntry.created_at.desc())
    prompts = db.session.scalars(stmt).all()
    all_tags = db.session.scalars(select(Tag).order_by(Tag.name)).all()
    
    return render_template('main/index.html', prompts=prompts, all_tags=all_tags, q=q, tag_name=tag_name)


@main.route('/prompt/new', methods=['GET', 'POST'])
@login_required
def prompt_new():
    form = PromptEntryForm()
    if form.validate_on_submit():
        tag_names = [t.strip().lower() for t in form.tags.data.split(',') if t.strip()]
        tags_list = []
        for name in tag_names:
            tag = Tag.query.filter_by(name=name).first()
            if not tag:
                tag = Tag(name=name)
                db.session.add(tag)
            tags_list.append(tag)
            
        prompt = PromptEntry(
            title=form.title.data,
            original_prompt=form.original_prompt.data,
            negative_prompt=form.negative_prompt.data or None,
            author=current_user,
            tags=tags_list
        )
        db.session.add(prompt)
        db.session.commit()
        flash('Prompt başarıyla oluşturuldu!', 'success')
        return redirect(url_for('main.index'))
    return render_template('prompt_form.html', title='Yeni Prompt', form=form, is_edit=False)

@main.route('/prompt/<int:id>')
def prompt_detail(id):
    prompt = PromptEntry.query.get_or_404(id)
    return render_template('prompt.html', prompt=prompt)

@main.route('/prompt/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def prompt_edit(id):
    prompt = PromptEntry.query.get_or_404(id)
    if prompt.author != current_user:
        abort(403)
        
    form = PromptEntryForm(obj=prompt)
    if request.method == 'GET':
        form.tags.data = ', '.join([t.name for t in prompt.tags])
        
    if form.validate_on_submit():
        tag_names = [t.strip().lower() for t in form.tags.data.split(',') if t.strip()]
        tags_list = []
        for name in tag_names:
            tag = Tag.query.filter_by(name=name).first()
            if not tag:
                tag = Tag(name=name)
                db.session.add(tag)
            tags_list.append(tag)
            
        prompt.tags = tags_list
        prompt.title = form.title.data
        prompt.original_prompt = form.original_prompt.data
        prompt.negative_prompt = form.negative_prompt.data or None
        db.session.commit()
        flash('Prompt başarıyla güncellendi!', 'success')
        return redirect(url_for('main.prompt_detail', id=prompt.id))
        
    return render_template('prompt_form.html', title='Prompt Düzenle', form=form, is_edit=True, prompt=prompt)

@main.route('/prompt/<int:id>/delete', methods=['POST'])
@login_required
def prompt_delete(id):
    prompt = PromptEntry.query.get_or_404(id)
    if prompt.author != current_user:
        abort(403)
    db.session.delete(prompt)
    db.session.commit()
    flash('Prompt başarıyla silindi.', 'success')
    return redirect(url_for('main.index'))

@main.route('/diary')
@login_required
def diary():
    entries = current_user.diary_entries.order_by(AIDiaryEntry.created_at.desc()).all()
    return render_template('diary.html', title='AI Günlüğü', entries=entries)

@main.route('/diary/new', methods=['GET', 'POST'])
@login_required
def diary_new():
    form = AIDiaryEntryForm()
    # Populate user's own prompts as selection choices
    prompts_choices = [(-1, 'Seçilmedi')] + [(p.id, p.title) for p in current_user.prompts.order_by(PromptEntry.created_at.desc()).all()]
    form.prompt_entry_id.choices = prompts_choices
    
    pre_prompt_id = request.args.get('prompt_id', type=int)
    if request.method == 'GET' and pre_prompt_id:
        # Verify that pre-selected prompt belongs to current user
        p = PromptEntry.query.get(pre_prompt_id)
        if p and p.author == current_user:
            form.prompt_entry_id.data = pre_prompt_id
            
    if form.validate_on_submit():
        prompt_id = form.prompt_entry_id.data
        if prompt_id == -1:
            prompt_id = None
        else:
            prompt_check = PromptEntry.query.get(prompt_id)
            if not prompt_check or prompt_check.author != current_user:
                flash('Geçersiz prompt seçimi.', 'danger')
                return redirect(url_for('main.diary_new'))
                
        entry = AIDiaryEntry(
            title=form.title.data,
            content=form.content.data,
            author=current_user,
            prompt_entry_id=prompt_id
        )
        db.session.add(entry)
        db.session.commit()
        flash('Günlük girdisi başarıyla oluşturuldu!', 'success')
        return redirect(url_for('main.diary'))
        
    return render_template('diary_form.html', title='Yeni Günlük Girdisi', form=form, is_edit=False)

@main.route('/diary/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def diary_edit(id):
    entry = AIDiaryEntry.query.get_or_404(id)
    if entry.author != current_user:
        abort(403)
        
    form = AIDiaryEntryForm(obj=entry)
    prompts_choices = [(-1, 'Seçilmedi')] + [(p.id, p.title) for p in current_user.prompts.order_by(PromptEntry.created_at.desc()).all()]
    form.prompt_entry_id.choices = prompts_choices
    
    if request.method == 'GET':
        form.prompt_entry_id.data = entry.prompt_entry_id if entry.prompt_entry_id else -1
        
    if form.validate_on_submit():
        prompt_id = form.prompt_entry_id.data
        if prompt_id == -1:
            prompt_id = None
        else:
            prompt_check = PromptEntry.query.get(prompt_id)
            if not prompt_check or prompt_check.author != current_user:
                flash('Geçersiz prompt seçimi.', 'danger')
                return redirect(url_for('main.diary_edit', id=entry.id))
                
        entry.title = form.title.data
        entry.content = form.content.data
        entry.prompt_entry_id = prompt_id
        db.session.commit()
        flash('Günlük girdisi başarıyla güncellendi!', 'success')
        return redirect(url_for('main.diary'))
        
    return render_template('diary_form.html', title='Günlük Düzenle', form=form, is_edit=True, entry=entry)

@main.route('/diary/<int:id>/delete', methods=['POST'])
@login_required
def diary_delete(id):
    entry = AIDiaryEntry.query.get_or_404(id)
    if entry.author != current_user:
        abort(403)
    db.session.delete(entry)
    db.session.commit()
    flash('Günlük girdisi başarıyla silindi.', 'success')
    return redirect(url_for('main.diary'))


@main.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PromptForm()
    if form.validate_on_submit():
        tag_names = [t.strip().lower() for t in form.tags.data.split(',') if t.strip()]
        tags_list = []
        for name in tag_names:
            # SQLAlchemy 2.x query style
            tag = db.session.scalar(select(Tag).where(Tag.name == name))
            if not tag:
                tag = Tag(name=name)
                db.session.add(tag)
            tags_list.append(tag)
            
        prompt = PromptEntry(
            title=form.title.data,
            original_prompt=form.original_prompt.data,
            negative_prompt=form.negative_prompt.data or None,
            user_id=current_user.id
        )
        for tag in tags_list:
            prompt.tags.append(tag)
            
        db.session.add(prompt)
        db.session.commit()
        flash('Yeni sinematik prompt başarıyla oluşturuldu!', 'success')
        return redirect(url_for('main.index'))
    return render_template('main/create_prompt.html', title='Yeni Prompt Ekle', form=form)


