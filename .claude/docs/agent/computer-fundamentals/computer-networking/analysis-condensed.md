# computer-networking Condensed Notes

## Summary

- Project name: computer-networking
- Project path: `D:\claude-code-sourcemap\.claude\docs\agent\computer-fundamentals\computer-networking`
- Document type: agent
- Purpose: provide condensed routing notes for answering computer-networking questions from this knowledge base

## Source Routing

- `图解网络-小林coding-v4.0.epub`
  - Best for: interview-oriented explanation, packet journey, HTTP/HTTPS, Linux receive/send path
  - Use when: user asks for practical intuition, end-to-end request flow, or high-frequency interview framing
- `图解 HTTP`
  - Best for: HTTP semantics, cache, cookies, status codes, connection evolution, HTTPS positioning
  - Use when: user asks application-layer behavior or browser/server interaction
- `图解 TCP/IP`
  - Best for: protocol stack intuition, addressing, packet flow, common device roles
  - Use when: user needs entry-level but accurate conceptual model
- `网络是怎样连接的`
  - Best for: narrative packet journey from browser to server and back
  - Use when: user asks “输入网址后发生了什么”
- `计算机网络：自顶向下方法`
  - Best for: systematic textbook structure and course-style explanation
  - Use when: user wants complete topic framing or academically organized answer
- `TCP/IP 详解 卷一：协议`
  - Best for: field-level protocol details, packet behavior, implementation-oriented depth
  - Use when: user asks header fields, handshake details, retransmission/window behavior
- `The TCP/IP Guide`
  - Best for: broad protocol reference and cross-protocol lookup
  - Use when: a topic spans multiple protocol families and needs quick structured recall
- `RFC`
  - Best for: normative definitions and exact protocol semantics
  - Use when: precision matters, definitions conflict, or edge cases are important

## Preferred Explanation Order

- Start from the user-visible problem
- Map the problem to protocol layer boundaries
- Explain end-to-end flow before drilling into fields
- Separate textbook abstraction from actual engineering path
- Use RFC-level language only when precision is required

## Canonical Topic Map

- Layering: application, transport, network, link; explain why layering exists before listing models
- Packet journey: URL -> DNS -> TCP -> TLS -> HTTP -> response -> rendering boundary
- HTTP/HTTPS: semantics first, then performance evolution, then TLS coupling
- TCP/UDP: service model first, then reliability/congestion/ordering tradeoffs
- IP/MAC/ARP/routing/switching: always distinguish local delivery from cross-network forwarding
- DNS: resolution system, cache hierarchy, recursive vs iterative; not data forwarding
- Congestion vs flow control: define “whose bottleneck” before mechanisms
- Linux network path: connect socket, kernel stack, NIC, interrupt/DMA, receive queue if needed

## Common Confusions

- OSI vs TCP/IP
  - Prefer TCP/IP or five-layer explanation; mention OSI only as teaching mapping
- HTTP vs HTTPS vs TLS
  - HTTP is application semantics; HTTPS is HTTP over TLS
- DNS vs routing
  - DNS finds destination mapping; routing forwards packets
- MAC forwarding vs IP routing
  - L2 local forwarding vs L3 cross-network forwarding
- Flow control vs congestion control
  - Receiver capacity vs network capacity
- Reliable transport vs successful business request
  - TCP reliability does not guarantee app-level success

## Answering Heuristics

- If user asks “是什么”, prefer intuitive definition plus what problem it solves
- If user asks “为什么这样设计”, use textbook/system tradeoff framing
- If user asks “过程”, answer with ordered packet journey
- If user asks “区别”, compare service model, guarantees, overhead, and use cases
- If user asks “底层原理”, move from abstraction to headers/state machine/kernel path
- If user asks for exactness, mention RFC as source-of-truth and avoid over-claiming

## Knowledge Base Direction

- User docs should remain narrative and explanatory
- Agent docs should keep routing notes, confusion pairs, and preferred explanation sequences
- Future networking subtopics should split into dedicated files under packet journey, transport, application, routing, and kernel path
