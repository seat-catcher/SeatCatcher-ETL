# TODO
## sqlmodel 사용해서 MySQL RDS에 데이터 저장하기
## mysqldump를 통해 RDS에 저장된 지하철 데이터 추출하기 -> 로컬 개발 환경에 필요
## 아마 EC2 접속해서 해야할듯
```shell
mysqldump -h your-rds-endpoint \
          -u your-user -p \
          --no-create-info \
          --skip-triggers \
          your_db_name train_station > train_station_data.sql
```