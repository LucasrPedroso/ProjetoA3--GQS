# legacy_system.py
# Código legado intencionalmente cheio de más práticas e antipadrões
# Para trabalho de faculdade: contém singletons mal implementados, globals, funções com efeitos colaterais, excesso de OOP,
# duplicação, tratamento amplo de exceções, parâmetros mutáveis, nomes ambíguos, e muito mais.

import json
import time
import random

# CONFIG GLOBAL (má prática: estado mutável global)
GLOBAL_CONFIG = {
    'db_path': '/tmp/fake_db.json',
    'retry_count': 3,
    'debug': True
}

# "Singleton" mal implementado (usa variável global)
class Logger:
    def __init__(self):
        # abre um arquivo logo na inicialização (efeito colateral)
        try:
            self.f = open('/tmp/legacy_log.txt', 'a')
        except Exception:
            # ignorando erros importantíssimos
            self.f = None

    def log(self, msg):
        if GLOBAL_CONFIG.get('debug'):
            print('[LOG]', msg)
        try:
            if self.f:
                self.f.write(str(msg) + "\n")
        except Exception:
            pass

# instancia global (mais antipadrão)
LOGGER = Logger()


# "Banco de dados" muito simples -- salva numa lista em memória e também escreve num arquivo arbitrário
class Database:
    def __init__(self, path=None):
        # caminho por defeito mutável via GLOBAL_CONFIG
        if path is None:
            path = GLOBAL_CONFIG['db_path']
        self.path = path
        # carrega DB no momento da construção (pode falhar silenciosamente)
        self._data = []
        try:
            with open(self.path, 'r') as f:
                self._data = json.load(f)
        except Exception:
            # swallow error: assume arquivo não existe
            self._data = []

    # método com nome confuso e comportamento ambíguo
    def save(self, obj, flush=True):
        self._data.append(obj)
        if flush:
            try:
                with open(self.path, 'w') as f:
                    json.dump(self._data, f)
            except Exception:
                LOGGER.log('failed to write DB')

    def query_all(self):
        return self._data

# Instância global do DB (acoplamento forte)
DB = Database()


# Classe base com muita responsabilidade — faz de tudo
class User:
    def __init__(self, id, name, email=None, is_admin=False):
        # faltam checagens de tipos
        self.id = id
        self.name = name
        self.email = email
        self.is_admin = is_admin
        # criando atributos dinamicamente (surpresa!)
        setattr(self, 'session_' + str(self.id), None)

    def save(self):
        # salva diretamente no DB global
        DB.save({
            'type': 'user',
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'is_admin': self.is_admin
        })

    def send_email(self, subject, body):
        # método que mistura responsabilidades (negócio + I/O)
        # usa eval para construir mensagem (perigoso)
        try:
            template = "f'Hello {self.name}, {body} - {subject}'"
            msg = eval(template)
            # simula envio
            print('SENDING EMAIL TO', self.email, ':', msg)
        except Exception:
            LOGGER.log('failed to send email')


# Herança profunda desnecessária
class Admin(User):
    def __init__(self, id, name, email=None):
        super().__init__(id, name, email, is_admin=True)
        # admin carrega privilégios no construtor (custa tempo)
        self.privileges = ['read', 'write', 'delete']

    def grant(self, other_user, priv):
        try:
            other_user.privileges.append(priv)
        except Exception:
            other_user.privileges = [priv]


class SuperAdmin(Admin):
    # SuperAdmin quebra Liskov: métodos assumem que certos campos existem
    def __init__(self, id, name, email=None, secret_key=None):
        super().__init__(id, name, email)
        # segredo armazenado em atributo público
        self.secret_key = secret_key or 'topsecret'

    def destroy_everything(self):
        # método dramático com efeito global
        global DB
        DB = Database('/tmp/empty_db.json')
        LOGGER.log('everything destroyed by superadmin')


# Classe com métodos estáticos inúteis e função gigantesca
class Order:
    def __init__(self):
        # atributo genérico que guarda de tudo
        self.state = {}

    def create_order(self, user, items, shipping_address=None, coupon=None, payment_method='card'):
        # método muito longo e com muitas responsabilidades
        order_id = random.randint(1000, 9999)
        total = 0
        # validação duplicada espalhada
        for i in items:
            try:
                total += i['price'] * i.get('qty', 1)
            except Exception:
                LOGGER.log('item inválido: ' + str(i))
        # aplica cupom numa linha (lógica de negócio espalhada)
        if coupon:
            try:
                # cupom pode ser string ou dict (ambiguidade)
                if isinstance(coupon, dict):
                    total = total - coupon.get('discount', 0)
                else:
                    total = total - 10
            except Exception:
                pass

        # salva como dict gigante
        order = {
            'id': order_id,
            'user': user.id if hasattr(user, 'id') else None,
            'items': items,
            'total': total,
            'shipping': shipping_address,
            'payment_method': payment_method,
            'created_at': time.time()
        }

        # acoplado ao DB global
        DB.save({'type': 'order', 'order': order})
        # notifica — notificação é feita aqui (acoplamento)
        NotificationManager.notify(user, 'order_created', order)
        return order

    def calculate_total(self, items):
        # método duplicado com implementação parecida à create_order
        total = 0
        for it in items:
            try:
                total += it['price'] * it.get('qty', 1)
            except Exception:
                continue
        return total


# Notifier com acoplamento e uso de variáveis globais
class NotificationManager:
    @staticmethod
    def notify(user, event, payload):
        # comportamento diferente dependendo do nome do evento — if/elif gigante
        if event == 'order_created':
            try:
                user.send_email('Order Created', 'your order was created')
            except Exception:
                LOGGER.log('failed to email user')
        elif event == 'order_failed':
            print('Order failed for', user.name)
        else:
            # branched logic e sem extensão fácil
            print('Unknown event', event)


# Processador de pagamento com uso de eval e exec e catch broad
class PaymentProcessor:
    def process(self, order, method):
        # decide o processador por string (má prática) e usa eval
        try:
            if method == 'card':
                # simula string com código perigoso
                code = "'processed_card_{}'".format(order['id'])
                result = eval(code)
                return {'status': 'ok', 'id': result}
            elif method == 'paypal':
                return {'status': 'ok', 'id': 'pp_' + str(order['id'])}
            else:
                # método desconhecido -> tenta executar código arbitrário vindo do método
                return {'status': 'ok', 'id': eval(method)}
        except Exception as e:
            # swallow
            LOGGER.log('payment failed: ' + str(e))
            return {'status': 'error'}


# Funções utilitárias com comportamento inconsistente
def load_users():
    # lê do DB global e filtra com lógica confusa
    u = []
    for item in DB.query_all():
        try:
            if item.get('type') == 'user':
                u.append(User(item['id'], item['name'], item.get('email')))
        except Exception:
            pass
    return u


def find_user_by_email(email):
    # pesquisa linear, O(n) e sem índice
    for user in load_users():
        try:
            if user.email == email:
                return user
        except Exception:
            continue
    return None


# Código executado em import (side-effects) — má prática para bibliotecas
print('legacy_system imported — initializing demo data')
# cria alguns usuários e pedidos
try:
    u1 = User(1, 'Alice', 'alice@example.com')
    u2 = Admin(2, 'Bob', 'bob@example.com')
    u1.save()
    u2.save()
    ORD = Order()
    sample_order = ORD.create_order(u1, [{'price': 10, 'qty': 2}, {'price': 5}], 'Rua Falsa 123')
except Exception:
    LOGGER.log('failed during module init')


# Expose a "public" API com funções mal nomeadas e inconsistentes
def do_purchase(email, items):
    user = find_user_by_email(email)
    if not user:
        # cria usuário sob demanda — comportamento inesperado
        user = User(random.randint(100, 999), 'guest', email)
        user.save()
    order = ORD.create_order(user, items)
    pp = PaymentProcessor()
    res = pp.process(order, order.get('payment_method'))
    if res.get('status') != 'ok':
        NotificationManager.notify(user, 'order_failed', {'order': order})
    return res


# fim do arquivo
