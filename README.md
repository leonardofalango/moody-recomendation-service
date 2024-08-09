# 🌟 **Moody API** 🚀

Bem-vindo à **Moody API**, um serviço backend inovador de recomendação personalizada! 🌈✨

## 💡 **Sobre o Projeto**

**Moody** é uma API projetada para oferecer recomendações personalizadas com base em interações do usuário e preferências. Nosso objetivo é fornecer uma plataforma flexível e eficiente para gerenciar usuários, lugares e labels, e, assim, criar experiências mais ricas e adaptadas às necessidades de cada usuário.

---

## 🌐 **Base API Link**

- **The API is hosted at**: [https://moody-recomendation-service.vercel.app](https://moody-recomendation-service.vercel.app)
- **You can find the API documentation here**: [https://moody-recomendation-service.vercel.app/docs](https://moody-recomendation-service.vercel.app/docs)

---

## 📦 **Endpoints**

### 🏠 **Root**
- **GET /**: Read Root

### 📊 **Status**
- **GET /v1/status**: Status do sistema

---

## 👤 **Usuários**

### 📄 **Consultar Usuários**
- **GET /user/get_page/{pagination}**: Obtenha todos os usuários com paginação

### ✏️ **Criar Usuário**
- **POST /user/create**: Crie um novo usuário

### 🔍 **Buscar Usuário**
- **GET /user/get/{user_id}**: Obtenha um usuário pelo ID

### ✏️ **Atualizar Usuário**
- **PATCH /user/update/{user_id}**: Atualize informações de um usuário

### 🗑️ **Excluir Usuário**
- **DELETE /user/delete/{user_id}**: Exclua um usuário pelo ID

---

## 🌍 **Lugares**

### 🤝 **Interagir com Lugar**
- **POST /place/interact/**: Interaja com um lugar

### ❤️ **Curtir Lugar**
- **POST /place/like/{user_id}/{place_id}**: Curta um lugar

### 📋 **Consultar Todos os Lugares**
- **GET /place/get/all**: Obtenha todos os lugares

### ✏️ **Criar Lugar**
- **POST /place/create**: Crie um novo lugar

### 🔍 **Buscar Lugar**
- **GET /place/get/{place_id}**: Obtenha um lugar pelo ID

### ✏️ **Atualizar Lugar**
- **PATCH /place/update/{place_id}**: Atualize informações de um lugar

### 🗑️ **Excluir Lugar**
- **DELETE /place/delete/{place_id}**: Exclua um lugar pelo ID

---

## 🏷️ **Labels**

### 📋 **Consultar Todos os Labels**
- **GET /label/get/all**: Obtenha todos os labels

### ✏️ **Criar Label**
- **POST /label/create**: Crie um novo label

### 🔍 **Buscar Label**
- **GET /label/get/{label_id}**: Obtenha um label pelo ID

### ✏️ **Atualizar Label**
- **PATCH /label/update/{label_id}**: Atualize informações de um label

### 🗑️ **Excluir Label**
- **DELETE /label/delete/{label_id}**: Exclua um label pelo ID

---

## 🎯 **Recomendações**

### 🔍 **Obter Parâmetros de Recomendação**
- **GET /recommendation/{user_id}**: Obtenha parâmetros de recomendação para um usuário

### 🗑️ **Limpar Cache de Recomendação**
- **DELETE /recommendation/clear_cache/**: Limpe o cache de recomendações

---

## 📜 **Schemas**

Aqui estão alguns dos schemas utilizados na API:

- **Interaction**
- **Label**
- **Metrics**
- **Place**
- **User**
- **ValidationError**

---

## 🚀 **Como Começar**

1. **Configuração**: Clone este repositório e instale as dependências com `pip install -r requirements.txt`.
2. **Executar**: Inicie o servidor com `uvicorn main:app --reload`.
3. **Explorar**: Navegue até [https://moody-recomendation-service.vercel.app/docs](https://moody-recomendation-service.vercel.app/docs) para acessar a documentação interativa e começar a fazer chamadas à API!

---

**Moody** está aqui para transformar dados em recomendações significativas e ajudar você a criar experiências personalizadas incríveis. Se precisar de suporte ou tiver sugestões, não hesite em nos contatar! 🎉💬

**Happy Coding!** 🌟
