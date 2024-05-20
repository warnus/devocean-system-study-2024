# Spring Cloud Gateway로 Rate limiter 구현하기

### API Server setting

간단한 spring application 생성

```groovy
implementation("org.springframework.boot:spring-boot-starter-web")
```

```java
@RestController
@RequestMapping("/v1")
@RequiredArgsConstructor
public class HelloController {

    private final HelloService helloService;

    @GetMapping("/hello")
    public String sayHello() {
        return helloService.sayHello();
    }
}

```

### Gateway Server setting

`spring-boot-starter-data-redis-reactive` 을 사용하여 rate limiter를 구현하기 때문에 아래와 같이 의존성 추가

- 토큰 버킷 알고리즘으로 구현됨
  - [request_rate_limiter.lua](https://github.com/spring-cloud/spring-cloud-gateway/blob/af09c72a9a/spring-cloud-gateway-server/src/main/resources/META-INF/scripts/request_rate_limiter.lua)

```groovy
implementation 'org.springframework.cloud:spring-cloud-starter-gateway'
implementation 'org.springframework.boot:spring-boot-starter-data-redis-reactive'
```
### KeyReslover
``` java
@Component
public class UserIdKeyResolver implements KeyResolver {
    @Override
    public Mono<String> resolve(ServerWebExchange exchange) {
        String userId = exchange.getRequest()
                .getHeaders()
                .getFirst("X-USER-ID");
        assert userId != null;
        return Mono.just(userId);
    }
}
```

### application.yml 설정

 `429 Too Many Requests` 를 테스트할 수 있는 설정 값

![result](https://github.com/warnus/devocean-system-study-2024/assets/58351498/108c7f9e-8e32-4ddb-a062-37c349d49e4e)

- 처리된 요청의 응답
  
    ![okok](https://github.com/warnus/devocean-system-study-2024/assets/58351498/6340e4fa-190f-4dfb-9576-dd0ed871cc32)
  
- 버려진 요청의 응답
  
    ![toomany](https://github.com/warnus/devocean-system-study-2024/assets/58351498/b8267259-fd9f-4d1e-a6cb-a9003c10f92c)

1초마다 1개씩 버킷 (용량=100)에 토큰이 추가됨

하지만, 요청 당 100개의 토큰을 소모하게 되어 바로 다음의 요청은 토큰 개수가 부족하기 때문에 버려지게 됨

```yaml
server:
  port: 8081 # 로컬에서 API 서버와 같이 돌려서 포트 변경

spring:
  application:
    name: api-gateway
  cloud:
    gateway:
       routes:
          - id: backend-all
            uri: http://localhost:8080
            filters:
              - name: RequestRateLimiter
                args:
                  redis-rate-limiter.replenishRate: 1
                  redis-rate-limiter.burstCapacity: 100 
                  redis-rate-limiter.requestedTokens: 100
                  key-resolver: "#{@userIdKeyResolver}" # KeyResolver 인터페이스를 구현한 클래스의 bean 이름 지정
            predicates:
              - Path=/**
              - Method=GET
  data:
    redis:
      host: localhost
      port: 6379
      database: 0
```

- `redis-rate-limiter.replendishRate`:  how many requests **per second** to allow (without any dropped requests). This is the rate at which the token bucket is filled.
- `redis-rate-limiter.burstCapacity` : the maximum number of requests a user is allowed in a single second (without any dropped requests). This is the number of tokens the token bucket can hold. Setting this value to zero blocks all requests.
- `redis-rate-limiter.requestedTokens` : how many tokens a request costs. This is the number of tokens taken from the bucket for each request and defaults to `1`.

Redis에 request_rate_limiter.{userId}.tokens, request_rate_limiter.{userId}.timestamp 2개의 key가 저장됨

![image](https://github.com/warnus/devocean-system-study-2024/assets/58351498/91f9af5f-444b-4351-9395-0fb3d593cf31)

- request_rate_limiter.{userId}.tokens: 해당 userId의 버킷 안에 토큰이 얼마나 남았는지
- request_rate_limiter.{userId}.timestamp: 가장 최근 요청의 타임스탬프
