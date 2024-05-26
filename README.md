#1 Get Started

```bash
$ git clone (repo주소)
---- 하위 폴더 이동
$ python -m venv venv
$ source venv/Scripts/activate
---- 백엔드
$ pip install -r requirements.txt (장고 및 설치패키지)
$ python manage.py makemigrations
$ python manage.py migrate (데이터베이스에 모델 반영)
$ python manage.py runserver (서버 실행)
---- 프론트엔드
$ npm install (Vue 및 설치패키지)
$ npm run dev (서버 실행)
```

#2-1 Vue

![vue](https://github.com/OneDayOneAlgorithm/Kim_movie/assets/104268939/f3085285-eae9-4e66-af97-e7f54cb6196e)



#2-2 Template & Components



![client_view](https://github.com/OneDayOneAlgorithm/Kim_movie/assets/104268939/fecc057b-1897-4e60-b692-8e83546f08d9)



#2-3 ERD



![movie_db](https://github.com/OneDayOneAlgorithm/Kim_movie/assets/104268939/f0498ca9-ada6-47a2-8909-25a6e13024d8)



#2-4 목표

- 사용자 경험 최적화를 위한 UI/UX, DB 설계

- 유저별 선호 장르와 조회수를 기반으로 영화 추천 알고리즘 구현

- git을 사용한 개발 및 병합, 피드백

- vuetify와 css를 활용한 반응형 웹 어플리케이션 제작

- 백엔드, 프론트엔드 역할 배분



#2-5 팀원 및 업무 분담 내역



곽효선: 추천 알고리즘 설계, 백엔드 DB 구현 및 API 설계



안현성: 프론트엔드 UI/UX 설계 및 Detail 페이지, Article 페이지 설계



#3 핵심 기능 & 디자인



main page

![main_page](https://github.com/OneDayOneAlgorithm/Kim_movie/assets/104268939/6dcdf9ed-2760-427b-83a7-6fd2f2a3db7d)



login & signup



![log_in](https://github.com/OneDayOneAlgorithm/Kim_movie/assets/104268939/6aaaf50c-f526-49aa-b1a4-39d41ed9beae)
<img src="https://github.com/OneDayOneAlgorithm/Kim_movie/assets/104268939/f8de3b39-b74c-45da-ac9b-77ed5b5bd9dc" title="" alt="sign_up" width="477">



profile & profile update



![my_profile](https://github.com/OneDayOneAlgorithm/Kim_movie/assets/104268939/59e4071e-19e9-44d2-955d-4230a1025a7f)


<img src="https://github.com/OneDayOneAlgorithm/Kim_movie/assets/104268939/df7b114f-a097-47cd-b033-be511b91421e" title="" alt="other_user_profile" width="653">



![profile_update_view](https://github.com/OneDayOneAlgorithm/Kim_movie/assets/104268939/be4a6dd4-9f93-433f-b70d-4f0f855e92f8)



detail page



![detail_page](https://github.com/OneDayOneAlgorithm/Kim_movie/assets/104268939/584cc76c-04df-45ce-9c6d-ca3cc5bcea7b)



trailer



![trailer](https://github.com/OneDayOneAlgorithm/Kim_movie/assets/104268939/ea383a71-36c6-4cc1-9a1f-e552b484b99b)



review & review detail



![review_component](https://github.com/OneDayOneAlgorithm/Kim_movie/assets/104268939/1aa724ae-8974-4c9e-969a-142d8238193e)
![review_detail_page](https://github.com/OneDayOneAlgorithm/Kim_movie/assets/104268939/29bc57b4-d06a-46e7-b1f3-21de3f91fef0)



#4 소감



곽효선:

학기말 프로젝트로 영화 추천 사이트를 제작하게 된 것은 정말 흥미로운 경험이었습니다. 이 프로젝트는 단순히 코딩 기술을 적용하는 것을 넘어,사용자가 어떤 영화를 선호하는지, 어떤 요소가 그들의 선택에 영향을 미치는지에 대해 깊게 고민해보는 계기가 되었습니다.
사용자의 취향과 요구를 이해하고, 이를 기반으로 개인화된 추천을 제공하는 알고리즘을 설계하는 과정은 쉽지 않았습니다.하지만 이 과정에서 데이터 분석, 
사용자 경험 디자인 등 다양한 영역의 지식을 획득하게 되었고, 이는 저에게 큰 자산이 되었습니다. 또한, 프로젝트를 진행하면서 협업의 중요성을 깨달았습니다.
서로 다른 아이디어를 통합하고, 시너지를 창출하는 과정에서 팀원의 다양한 의견을 수용하고 이해하는 능력이 중요하다는 것을 느꼈습니다. 그래서 저는 이를 통해 더욱 성장한 것 같습니다.
1학기의 마지막이지만 마지막이라는 것은 새로운 시작을 알리는 것과 같습니다. 앞으로 더 열심히하여 2학기에는 지금보다 더 성장하는 마음과 배움의 자세로 임하겠습니다.



안현성:

이번 학기 말 프로젝트로 영화 추천 사이트를 제작하게 된 것은 흥미로우면서도 깊은 성장의 기회가 되었습니다. 팀원 두 명이서 백엔드와 프론트엔드를 나눠서 작업하였는데, 저는 프론트엔드 개발을 주로 담당하게 되었습니다.
사용자와 직접 소통하는 프론트엔드 개발을 담당하면서, 사용자 경험에 대해 깊이 생각해볼 수 있는 기회가 되었습니다. 사용자의 행동 패턴, 취향, 그리고 요구를 이해하고 이를 반영한 디자인과 기능을 구현하는 과정은 쉽지 않았지만, 그만큼 저에게 큰 성장을 가져다주었습니다.
또한, 백엔드를 담당한 팀원과의 협업도 큰 배움이었습니다. 서로 다른 분야에서 작업을 하면서도 효율적인 소통과 협력을 통해 시너지를 창출해내는 경험은 앞으로의 팀 프로젝트에서도 큰 도움이 될 것이라 확신합니다.
이 프로젝트를 통해 제가 배운 것, 경험한 것은 많습니다. 하지만 무엇보다 가장 값진 것은 '사용자를 위한 제품'을 만드는 것의 진정한 의미를 깨달았다는 것입니다. 앞으로의 공부와 경력에서 이 경험을 바탕으로 사용자 중심의 서비스를 제공하는 개발자가 되겠습니다.
