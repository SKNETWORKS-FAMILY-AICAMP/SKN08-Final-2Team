# 사용하는 Golang 버전에 맞추도록 합니다 (학원 컴에서 구성한 것의 경우 1.23 버전이였던 것으로 기억함)
FROM golang:1.20-alpine AS builder

WORKDIR /app

# 의존성 복사 및 설치
COPY go.mod go.sum ./
RUN go mod download

# 소스 전체 복사
COPY . .

# main 패키지에서 빌드
RUN go build -o fiber-app ./main

# Run stage
FROM alpine:latest

WORKDIR /root/

# 바이너리 복사
COPY --from=builder /app/fiber-app .
COPY .env ./

# 포트 환경 변수로 지정
ENV FIBER_PORT=3773
EXPOSE ${FIBER_PORT}

CMD ["./fiber-app"]
