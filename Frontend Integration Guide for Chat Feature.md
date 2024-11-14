# Frontend Integration Guide for Real-time Chat System

This guide provides detailed instructions for integrating the backend chat features using Socket.IO in the Angular frontend.

## 1. Connecting to the WebSocket Server

Use `Socket.IO-client` to connect to the backend:

```typescript
import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  constructor(private socket: Socket) { }

  connect() {
    this.socket.connect();
  }

  disconnect() {
    this.socket.disconnect();
  }

  onConnect() {
    return this.socket.fromEvent('connected');
  }

  joinRoom(roomId: number) {
    this.socket.emit('join', { room: roomId });
  }

  leaveRoom(roomId: number) {
    this.socket.emit('leave', { room: roomId });
  }

  sendMessage(roomId: number, message: string) {
    this.socket.emit('message', { room: roomId, message });
  }

  onMessage() {
    return this.socket.fromEvent('message');
  }

  onProductShared() {
    return this.socket.fromEvent('product_shared');
  }
}
```

## 2. Displaying Messages in the Chat

```html
<!-- chat.component.html -->
<div *ngFor="let message of messages">
  <p>{{ message.user }}: {{ message.msg }}</p>
</div>

<input [(ngModel)]="newMessage" placeholder="Type a message..." />
<button (click)="sendMessage()">Send</button>
```

```typescript
// chat.component.ts
import { Component, OnInit } from '@angular/core';
import { ChatService } from './chat.service';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
})
export class ChatComponent implements OnInit {
  messages: any[] = [];
  newMessage: string = '';

  constructor(private chatService: ChatService) {}

  ngOnInit() {
    this.chatService.connect();
    
    this.chatService.onMessage().subscribe((message) => {
      this.messages.push(message);
    });
  }

  sendMessage() {
    this.chatService.sendMessage(1, this.newMessage);  // Replace with actual room ID
    this.newMessage = '';
  }
}
```

## 3. Handling Product Sharing in the Chat

To handle shared products, the frontend should listen to the `product_shared` event:

```html
<!-- chat.component.html -->
<div *ngFor="let message of messages">
  <p *ngIf="!message.product">{{ message.user }}: {{ message.msg }}</p>
  
  <!-- Display shared product details -->
  <div *ngIf="message.product">
    <h4>{{ message.product.name }}</h4>
    <p>{{ message.product.description }}</p>
    <p>Price: {{ message.product.price }}</p>
    <img [src]="message.product.image_url" alt="Product Image">
  </div>
</div>
```

```typescript
ngOnInit() {
  this.chatService.onProductShared().subscribe((productMessage) => {
    this.messages.push({
      user: productMessage.user,
      product: productMessage.product
    });
  });
}
```

---
