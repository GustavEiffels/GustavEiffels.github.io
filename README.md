# Singsiuk LAB

Personal laboratory for investment analysis and technical research.

## Owner Mode (방문자 카운트 본인 제외)

사이트 방문자 카운트에서 본인을 제외하려면, 브라우저 개발자 도구 콘솔(`F12` → Console)에서 아래 명령어를 **한 번만** 실행하세요.

```javascript
localStorage.setItem('site_owner', 'true')
```

실행 후 새로고침하면 사이드바에 **👁 owner mode** 가 표시되며, 이후 방문은 카운트에 포함되지 않습니다.

> 브라우저 localStorage를 초기화하거나 다른 브라우저/기기에서 접속 시 재설정이 필요합니다.
