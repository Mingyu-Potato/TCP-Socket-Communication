# mobile_RP22222D

# git 사용법 통일

다음의 과정으로 작업 수행 (git remote update 최신화)
1. git status  (현재 브랜치 상태 확인)
1. git pull origin main ( 마스터 최신화)
1. git checkout -b dev-task1 (새로운 브랜치 생성)
1. -----작업-----
1. git add -A (새로운 브랜치에서 작업한내용 add)
1. git commit -m "test" (커밋)
1. git push origin dev-task1 (원격저장소에 푸쉬)
1. -----풀리퀘생성 -----
1. -----merge-----
1. git checkout main (마스터 브랜치로 변경)
1. git pull origin main (새로수정된 마스터 브랜치로부터 수정내용  pull)
1. git branch -d dev-task1 (브랜치 삭제)
1. git push origin :dev-task1 (브랜치 삭제)

commit message는 한글로 작성,
git commit -m "close issue #21 어떤 문제 해결.
