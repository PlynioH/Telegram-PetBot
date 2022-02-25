from dataclasses import dataclass
import logging, json, os, string
from typing import *
from telegram import *
from telegram.ext import *
from peewee import *

(
    CriarConta,
    FazerLogin,
    TutorNome,
    TutorCpf,
    TutorIdade,
    TutorTelefone,
    TutorEndereco,
    TutorCep,
    TutorUsuario,
    TutorSenha,
    TutorUsuarioLogin,
    TutorSenhaLogin
) = map(chr, range(12))

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

db = PostgresqlDatabase(database=os.environ['DB_DATABASE'], user=os.environ['DB_USERNAME'], password=os.environ['DB_PASSWORD'], host=os.environ['DB_URL'], port=os.environ['DB_PORT'])

#models 
class Tutor(Model):
    nome = CharField(null=True)
    usuario = CharField(null=True, unique= True)
    senha = BigBitField(null=True)
    cpf = CharField(null=True)
    idade = IntegerField(null=True)
    telefone = CharField(null=True)
    endereco = CharField(null=True)
    cep = CharField(null=True)
    codtelegram = CharField(null=False)
    
    class Meta:
        database = db

class Pet(Model):
    nome = CharField(null=False)
    especie = CharField(null=True)
    raca = CharField(null=True)
    cor = CharField(null=True)
    sexo = CharField(null=True)
    porte = CharField(null=True)
    idade = IntegerField(null=True)
    peso = DoubleField(null=True)
    observacao = TextField(null=True)
    tutor_id = ForeignKeyField(Tutor, null=False,  backref='pets')
    
    class Meta:
        database = db
     
class Consulta(Model):
    data = CharField(null=True)
    hora = CharField(null=True)
    descricao = TextField(null=True)
    pet_id = ForeignKeyField(Pet, null=False,backref='consultas')
    
    class Meta:
        database = db

#commands
def say(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    message_id = int(update.message.message_id)
    print(update)
    context.bot.send_message(chat_id, text=update.message.text[4:])
    context.bot.delete_message(chat_id, message_id, timeout=None, api_kwargs=None)

def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    message_id = int(update.message.message_id)
    buttons = [
        [
            InlineKeyboardButton(text='Fazer login', callback_data=str(FazerLogin)),
            InlineKeyboardButton(text='Criar Conta', callback_data=str(CriarConta)),
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    context.bot.send_message(chat_id, text='Não detectamos nenhuma conta cadastrada no seu usuario escolha entre uma das opções a baixo', reply_markup=keyboard)
    context.bot.delete_message(chat_id, message_id, timeout=None, api_kwargs=None)

#Fluxo de Cadastro

def tutorCadastro(update: Update, context: CallbackContext) -> int:
    update.callback_query.edit_message_text(text='Qual é o seu nome?')
    return TutorNome

def tutorNome(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Digite seu cpf'
    )
    return TutorCpf

def tutorCpf(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Digite sua Idade: '
    )
    return TutorIdade

def tutorIdade(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Digite seu Telefone: '
    )
    return TutorTelefone

def tutorTelefone(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Digite seu Endereço: '
    )
    return TutorEndereco

def tutorEndereco(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Digite seu CEP: '
    )
    return TutorCep

def tutorCep(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Digite seu Usuário: '
    )
    return TutorUsuario

def tutorUsuario(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Digite sua Senha: '
    )
    return TutorSenha

def tutorSenha(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Fim de conversa'
    )
    return ConversationHandler.END

#Fluxo de Login
def tutorLogin(update: Update, context: CallbackContext) -> int:
    update.callback_query.edit_message_text(text='Digite seu usuario:')
    return TutorUsuarioLogin

def tutorUsuarioLogin(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Digite sua Senha: '
    )
    return TutorSenhaLogin

def tutorSenhaLogin(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Fim de conversa'
    )
    return ConversationHandler.END


def main() -> None:


    token = str(os.environ['TOKEN'])
    updater = Updater(token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("say", say))
    
    dispatcher.add_handler(CommandHandler("start", start))
    
    dispatcher.add_handler(ConversationHandler(
        entry_points=[
            CallbackQueryHandler(tutorCadastro, pattern='^' + str(CriarConta) + '$'),
            CallbackQueryHandler(tutorLogin, pattern='^' + str(FazerLogin) + '$'),
        ],
        states={
            TutorNome: [MessageHandler(Filters.text & ~Filters.command, tutorNome)],
            TutorCpf: [MessageHandler(Filters.text & ~Filters.command, tutorCpf)],
            TutorIdade: [MessageHandler(Filters.text & ~Filters.command, tutorIdade)],
            TutorTelefone: [MessageHandler(Filters.text & ~Filters.command, tutorTelefone)],
            TutorEndereco: [MessageHandler(Filters.text & ~Filters.command, tutorEndereco)],
            TutorCep: [MessageHandler(Filters.text & ~Filters.command, tutorCep)],
            TutorUsuario: [MessageHandler(Filters.text & ~Filters.command, tutorUsuario)],
            TutorSenha: [MessageHandler(Filters.text & ~Filters.command, tutorSenha)],
            TutorUsuarioLogin: [MessageHandler(Filters.text & ~Filters.command, tutorUsuarioLogin)],
            TutorSenhaLogin: [MessageHandler(Filters.text & ~Filters.command, tutorSenhaLogin)],
        },
        fallbacks=[
        ],
    ))
    
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':

    try:
        db.connect()
        db.create_tables([Tutor, Pet, Consulta])
    except Exception as e:
        print(e)

    main()