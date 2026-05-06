# Singsiuk LAB — Fragment 작성 규칙

이 프로젝트는 GitHub Pages 기반 단일 페이지 앱입니다.
`index.html`이 `loadContent(page)`로 `content/` 하위 HTML fragment를 fetch하여 `#content-target`에 주입합니다.

---

## Fragment 파일 구조

- 위치: `content/` 또는 `content/dev/`, `content/stocks/` 등 하위 디렉터리
- 파일은 완전한 HTML 문서가 아닌 **fragment**입니다 — `<html>`, `<head>`, `<body>` 태그 없음
- `<style>` 블록과 `<script>` 블록을 파일 안에 포함할 수 있습니다
  - `<script>`는 `loadContent()` 내부에서 자동으로 재실행됩니다

---

## 공통 CSS 클래스 (assets/css/style.css)

| 클래스 | 용도 |
|---|---|
| `.card` | 섹션 컨테이너 (hover 효과 포함) |
| `.badge.badge-tag` | 파란 태그 |
| `.badge.badge-date` | 초록 날짜 태그 |
| `.badge.badge-warning` | 노란 경고 태그 |
| `.point` | 인라인 강조 텍스트 (파란 배경) |
| `.terminal-window` | 코드블록 컨테이너 (macOS 스타일 dots 헤더) |
| `.grid` | 2열 그리드 레이아웃 |
| `blockquote` | 인용/강조 박스 (왼쪽 파란 보더) |

### 코드블록 작성 패턴
```html
<div class="terminal-window">
  <div class="terminal-header">
    <span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span>
    <span class="terminal-title">파일명 또는 설명</span>
  </div>
  <pre><code>코드 내용</code></pre>
</div>
```

---

## 인라인 코드 스타일

일반 텍스트 내 `<code>` 태그는 자동으로 아래 스타일이 적용됩니다:
- **JetBrains Mono** 폰트
- **파란색** 텍스트 (`--accent`) + 반투명 파란 배경 + 테두리
- `pre` 내부 코드블록에는 영향 없음 (`:not(pre) > code` 선택자)

---

## 마침표 뒤 자동 줄바꿈 규칙

`[class*="-callout"]`, `.callout` 클래스 요소에 `white-space: pre-line`이 적용됩니다.

**작성 규칙**: callout 및 설명 박스 내부에서 각 문장은 HTML 소스에서 별도 줄에 작성하세요.
그러면 마침표 뒤 다음 문장이 자동으로 줄바꿈되어 표시됩니다.

```html
<!-- 올바른 작성 예시 -->
<div class="aop-callout ok">
  <strong>결과</strong>
  비즈니스 로직과 공통 기능이 완전히 분리된다.
  개발자는 비즈니스에만 집중할 수 있다.
  공통 기능을 바꿀 때 한 곳만 수정하면 된다.
</div>
```

---

## TOC 네비게이션 (우측 하단 플로팅 버튼)

내용이 긴 fragment에는 반드시 TOC를 추가합니다.
`toggleTOC()` 함수는 `index.html`에 전역으로 정의되어 있으므로 fragment에서 바로 호출 가능합니다.

### TOC CSS — fragment `<style>` 블록에 포함
```css
.report-toc {
  position: fixed; top: 0; right: -300px; width: 280px; height: 100vh;
  background: var(--surface); border-left: 1px solid var(--border);
  padding: 40px 25px; z-index: 1001;
  transition: right 0.3s cubic-bezier(0.4,0,0.2,1);
  box-shadow: -10px 0 30px rgba(0,0,0,0.5); overflow-y: auto;
}
.report-toc.active { right: 0; }
.report-toc h3 { font-size: 1.1rem; color: var(--accent); margin-bottom: 25px; font-weight: 700; display: flex; align-items: center; gap: 10px; }
.report-toc ul { list-style: none; padding: 0; margin: 0; }
.report-toc li { margin-bottom: 12px; line-height: 1.4; }
.report-toc a { color: var(--text-muted); text-decoration: none; font-size: 0.9rem; transition: 0.2s; display: block; padding: 5px 0; }
.report-toc a:hover { color: var(--accent); transform: translateX(5px); }
.toc-backdrop {
  position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(0,0,0,0.6); backdrop-filter: blur(3px);
  z-index: 1000; display: none; opacity: 0; transition: opacity 0.3s ease;
}
.toc-backdrop.active { display: block; opacity: 1; }
.toc-toggle-btn {
  position: fixed; bottom: 30px; right: 30px; width: 56px; height: 56px;
  background: var(--accent); color: #fff; border: none; border-radius: 50%;
  font-size: 1.5rem; cursor: pointer; z-index: 1002;
  box-shadow: 0 4px 15px var(--accent-glow);
  display: flex; align-items: center; justify-content: center; transition: all 0.2s ease;
}
.toc-toggle-btn:hover { transform: scale(1.1) rotate(5deg); }
@media (max-width: 768px) {
  .toc-toggle-btn { bottom: 20px; right: 20px; width: 48px; height: 48px; font-size: 1.2rem; }
}
```

### TOC HTML — fragment 본문 끝에 추가
```html
<!-- 각 섹션 card에 id 부여 -->
<div class="card" id="section-name">...</div>

<!-- TOC Backdrop -->
<div id="toc-backdrop" class="toc-backdrop" onclick="toggleTOC()"></div>

<!-- TOC Panel -->
<nav id="report-toc" class="report-toc">
  <h3>📑 목차</h3>
  <ul>
    <li><a href="#section-name" onclick="toggleTOC()">1. 섹션 제목</a></li>
  </ul>
</nav>

<!-- Floating TOC Button -->
<button class="toc-toggle-btn" onclick="toggleTOC()">📑</button>
```

---

## URL 라우팅

`loadContent('dev/파일명')` 호출 시 URL이 `#dev/파일명` 형태로 자동 변경됩니다.
직접 URL 접근 및 브라우저 뒤로가기/앞으로가기 모두 지원됩니다.

---

## dev.html 목록 항목 추가 형식

새 fragment 추가 시 `content/dev.html` 목록에 아래 형식으로 추가합니다:

```html
<li>
  <a
    onclick="loadContent('dev/파일명')"
    style="color: var(--accent); cursor: pointer"
  >
    [YYYY-MM-DD] 제목
  </a>
</li>
```

---

## CSS 변수 (다크 테마)

```
--bg: #0f1117          배경
--surface: #1a1d27     카드 배경
--surface2: #21253a    보조 배경
--border: #2e3350      테두리
--accent: #5e81f4      강조 (파란)
--green: #2fb344       성공/OK
--red: #d63939         위험/Bad
--yellow: #f59e0b      경고/Warn
--text: #e2e8f0        본문
--text-muted: #8892b0  보조 텍스트
--code-bg: #141824     코드 배경
```
