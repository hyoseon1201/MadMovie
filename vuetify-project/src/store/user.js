import {defineStore} from 'pinia';
import {useRouter} from "vue-router";
import {computed, ref} from "vue";
import axios from "axios";

export const useAccountStore = defineStore('account', () => {
  const router = useRouter()
  const token = ref(localStorage.getItem('token'))
  const username = ref(localStorage.getItem('username'))
  const error = ref(false)

  const signUp = function (payload) {
    const username = payload.username
    const email = payload.email
    const password1 = payload.password1
    const password2 = payload.password2

    axios({
      method: 'post',
      url: `http://127.0.0.1:8000/accounts/signup/`,
      data: {
        username, email, password1, password2
      }
    })
      .then(() => {
        const password = password1
        console.log('회원가입이 완료되었습니다.')
        return login({username, password})

      })
      .catch(err => {
        error.value = err
      })
  }

  const login = async function (payload) {
    const username = payload.username
    const password = payload.password

    await axios({
      method: 'post',
      url: `http://127.0.0.1:8000/accounts/login/`,
      data: {
        username, password
      }
    })
      .then(res => {
        console.log('로그인이 성공적으로 완료되었습니다.')
        token.value = res.data.key
        localStorage.setItem('token', token.value)
        localStorage.setItem('username', username)
        router.go()
      })
      .catch(err => {
        console.log(err)
        throw err
      })
  }

  const getProfile = async function (username) {
    let url = `http://127.0.0.1:8000/user/profile/${username}/`

    try {
      const response = await axios({
        method: 'get',
        url: url,
        headers: {
          Authorization: `Token ${token.value}`,
        }
      });
      console.log(response.data);
      return response.data; // 데이터 반환
    } catch (err) {
      console.error(err)
      throw err
    }
  };

  const updateProfile = async function (username, profileData) {
    let url = `http://127.0.0.1:8000/user/profile/${username}/`

    try {
      const response = await axios({
        method: 'patch',
        url: url,
        headers: {
          Authorization: `Token ${token.value}`,
        },
        data: profileData
      })
      console.log('프로필 업데이트가 성공적으로 완료되었습니다.');
      return response.data;
    } catch (err) {
      console.error('프로필 업데이트 중 오류가 발생했습니다:', err);
      throw err
    }
  }

  const manageFollowing = async function (username, action) {
    let url = `http://127.0.0.1:8000/user/following/`
    try {
      const data = {}
      if (action === 'follow') {
        data.follow = username;
      } else if (action === 'unfollow') {
        data.unfollow = username;
      }

      const response = await axios({
        method: 'post',
        url: url,
        headers: {
          Authorization: `Token ${token.value}`,
        },
        data: data
      })

      console.log(`${action === 'follow' ? '팔로우' : '언팔로우'}가 성공적으로 완료되었습니다.`)
      return response.data
    } catch (err) {
      console.error(`${action === 'follow' ? '팔로우' : '언팔로우'} 중 오류가 발생했습니다:`, err)
      throw err
    }
  }

  const isFollowing = async function (username) {
    let url = `http://127.0.0.1:8000/user/is_following/${username}`;
    try {
      const response = await axios({
        method: 'get',
        url: url,
        headers: {
          Authorization: `Token ${token.value}`,
        }
      });

      console.log('팔로잉 여부 조회가 성공적으로 완료되었습니다.');
      return response.data;
    } catch (err) {
      console.error('팔로잉 여부 조회 중 오류가 발생했습니다:', err);
      throw err;
    }
  }

  const getFollowList = async function () {
    let url = `http://127.0.0.1:8000/user/follow_list/`;

    try {
      const response = await axios({
        method: 'get',
        url: url,
        headers: {
          Authorization: `Token ${token.value}`,
        }
      });
      console.log('팔로우 목록 조회가 성공적으로 완료되었습니다.');
      return response.data; // 팔로우 목록 데이터 반환
    } catch (err) {
      console.error('팔로우 목록 조회 중 오류가 발생했습니다:', err);
      throw err;
    }
  }

  const deleteAccount = async function () {
    // 사용자에게 계정 삭제를 최종 확인
    if (!confirm("계정을 정말로 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다.")) {
      return;
    }

    // 계정 삭제 API 엔드포인트
    let url = `http://127.0.0.1:8000/user/delete/`;

    try {
      const response = await fetch(url, {
        method: 'DELETE',
        headers: {
          Authorization: `Token ${token.value}`,
        },
      });

      // 성공적으로 계정이 삭제되었는지 확인
      if (response.ok) {
        // 성공 처리 로직, 예를 들어 로그아웃 시키거나 로그인 페이지로 리다이렉트
        console.log("계정이 성공적으로 삭제되었습니다.");
      } else {
        // 오류 처리 로직
        console.error("계정 삭제 중 오류가 발생했습니다.");
      }
    } catch (error) {
      console.error("계정 삭제 요청 중 오류가 발생했습니다:", error);
    }
  }

  const passwordChange = async function (payload) {
    const new_password1 = payload.new_password1;
    const new_password2 = payload.new_password2;

    try {
      const response = await axios.post('http://127.0.0.1:8000/accounts/password/change/', {
        new_password1: new_password1,
        new_password2: new_password2,
      }, {
        headers: {
          Authorization: `Token ${token.value}`,
        },
      });

      console.log('비밀번호 변경 성공:', response.data);
      router.back()
    } catch (error) {
      console.error('비밀번호 변경 중 오류 발생:', error);
    }
  }


  const isLogin = computed(() => token.value !== null);

  return {
    signUp,
    login,
    getProfile,
    updateProfile,
    manageFollowing,
    isFollowing,
    getFollowList,
    deleteAccount,
    passwordChange,
    token,
    isLogin,
    error,
    username
  }
}, {persist: true})
