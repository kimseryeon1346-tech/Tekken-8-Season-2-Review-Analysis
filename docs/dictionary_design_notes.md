# Tekken 8 Issue Tag Dictionary v0.2 design notes

## Validation basis

Core validation은 9개 keyword × 5건으로 45/45 완료되었고, defense는 별도 supplemental 5/5 TP로 유지했다.
Context keyword인 changes, patch, season, fighting은 단독 태깅에 사용하지 않았다.
Conditional keyword인 devs, character(s), moves는 특정 phrase/cue와 함께 있을 때만 태깅한다.

## Matching policy

- 모든 텍스트는 lowercase와 공백 정규화를 거친다.
- regex word boundary로 substring 오탐을 막는다.
- multi-word phrase와 직접 시스템 용어를 먼저 적용한다.
- 한 리뷰에 여러 tag를 허용한다.
- 추천 리뷰의 tag는 불만으로 자동 해석하지 않고 recommendation_group과 원문을 함께 본다.
- Heat의 비게임 관용구와 character/moves/devs의 단독 일반 언급을 제외한다.

## Tags

### T01 Offensive_Pressure

과도한 공격 우위, 압박, 강제 50/50 및 plus-frame 중심 gameplay 언급

- Validation: Core 및 defense manual notes에서 공격 우위·plus frame·50/50이 반복 확인됨
- Include: plus frame|50/50|coin flip|offense-heavy|overly aggressive|mindless rushdown
- Conditional: aggression|aggressive|offense|offensive|pressure|rushdown|mix-up + issue/gameplay cue
- Exclusion: unrelated numeric ratio|neutral use without an issue/gameplay cue
- Rule note: 일반 pressure/offense 단독은 제외하고 강제성·과도함·50/50·방어 약화 문맥이 있을 때만 태깅

### T02 Defense_Movement

방어 선택지, blocking, movement, sidestep, backdash 및 counterplay 약화 언급

- Validation: Defense supplemental 5/5 TP; POST 비추천 exact defense 304/3,766(8.07%)
- Include: defense|defence|defensive|sidestep|side step|backdash|back dash|KBD
- Conditional: movement|neutral|blocking + nerf/lack/punish/issue cue
- Exclusion: non-game idiom unrelated to Tekken defense or movement
- Rule note: movement/neutral/blocking 단독은 제외; 추천 리뷰의 개선·칭찬 문맥은 이슈 존재가 아닌 주제 언급으로 해석

### T03 Character_Homogenization

캐릭터 아키타입·장단점·정체성이 비슷해지거나 획일화됐다는 언급

- Validation: character 5/5 TP, characters 5/5 TP; 단독어의 다의성 때문에 Conditional
- Include: homogenize|homogenized|homogenization|homogenous|homogeneous
- Conditional: character|characters|roster + same/similar/identity/archetype/unique/strength/weakness
- Exclusion: character select|locked character|DLC character without identity/archetype context
- Rule note: character(s) 단독 및 구매·해금·단순 캐릭터명 언급은 제외

### T04 Heat_System

Tekken 8 Heat 시스템, mechanic, activation, engage 또는 관련 gameplay 언급

- Validation: heat 5/5 TP 및 고유 시스템 명칭으로 Issue 분류
- Include: heat|heat system|heat mechanic|heat engage|heat smash|heat burst|heat dash
- Conditional: (none)
- Exclusion: heat of the battle|heat of the moment when no Tekken system cue exists
- Rule note: 명백한 비게임 관용구만 제외; 추천 리뷰 태깅은 불만으로 자동 해석하지 않음

### T05 Moveset_Balance_Issue

기술 구성, frame data, tracking, off-axis, damage, buff/nerf 및 기술 버그 언급

- Validation: moves 5/5 TP였지만 일반어이므로 Conditional 분류
- Include: moveset|move set|off-axis|frame data
- Conditional: move|moves + removed/nerfed/buffed/broken/bug/damage/tracking/50-50/plus-frame cue
- Exclusion: new move praise or neutral move mention without balance/property cue
- Rule note: move(s) 단독과 단순 기술 설명은 제외하고 속성·밸런스·버그·강제 상황 문맥을 요구

### T06 Dev_Direction_Trust

개발 방향, 커뮤니티 피드백, 신뢰, 소통 및 개발진 판단에 대한 언급

- Validation: devs 5/5 TP였지만 긍정·중립 사용 가능성 때문에 Conditional
- Include: out of touch|lost faith|lost trust|ignore community|ignore feedback|not listening
- Conditional: dev|devs|developer|developers|Bandai Namco|Harada + feedback/trust/direction/listen/ignore/community cue
- Exclusion: developer credit or neutral developer mention without direction/trust cue
- Rule note: dev(s)/developer(s) 단독은 제외; 추천 리뷰에서 긍정적 소통 언급이면 불신으로 해석하지 않음
