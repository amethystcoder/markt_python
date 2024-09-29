# Frontend Integration Guide for Chat Feature

This guide provides detailed code samples and instructions for integrating the chat feature into the Angular frontend application.

## Setup

First, install the required dependencies:

```bash
npm install socket.io-client @types/socket.io-client
```

## Socket Service

Create a service to manage the WebSocket connection:

```typescript
// src/app/services/socket.service.ts
import { Injectable } from '@angular/core';
import { io, Socket } from 'socket.io-client';
import { BehaviorSubject, Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class SocketService {
  private socket: Socket;
  private connectionStatus = new BehaviorSubject<boolean>(false);

  constructor() {
    this.socket = io(environment.apiUrl, {
      autoConnect: false,
      withCredentials: true
    });

    this.socket.on('connect', () => this.connectionStatus.next(true));
    this.socket.on('disconnect', () => this.connectionStatus.next(false));
  }

  connect(token: string): void {
    this.socket.io.opts.extraHeaders = {
      Authorization: `Bearer ${token}`
    };
    this.socket.connect();
  }

  disconnect(): void {
    this.socket.disconnect();
  }

  joinRoom(roomId: string): void {
    this.socket.emit('join', { room: roomId });
  }

  leaveRoom(roomId: string): void {
    this.socket.emit('leave', { room: roomId });
  }

  sendMessage(roomId: string, message: string): void {
    this.socket.emit('message', { room: roomId, message });
  }

  shareProduct(roomId: string, productId: number): void {
    this.socket.emit('product_share', { room: roomId, product_id: productId });
  }

  onMessage(): Observable<any> {
    return new Observable(observer => {
      this.socket.on('message', (data) => observer.next(data));
    });
  }

  onProductShared(): Observable<any> {
    return new Observable(observer => {
      this.socket.on('product_shared', (data) => observer.next(data));
    });
  }

  onError(): Observable<any> {
    return new Observable(observer => {
      this.socket.on('error', (data) => observer.next(data));
    });
  }

  isConnected(): Observable<boolean> {
    return this.connectionStatus.asObservable();
  }
}
```

## Chat Component

Create a component to handle the chat UI:

```typescript
// src/app/components/chat/chat.component.ts
import { Component, OnInit, OnDestroy } from '@angular/core';
import { SocketService } from '../../services/socket.service';
import { AuthService } from '../../services/auth.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit, OnDestroy {
  messages: any[] = [];
  currentMessage = '';
  currentRoom: string | null = null;
  private subscriptions: Subscription[] = [];

  constructor(
    private socketService: SocketService,
    private authService: AuthService
  ) {}

  ngOnInit() {
    this.socketService.connect(this.authService.getToken());
    
    this.subscriptions.push(
      this.socketService.onMessage().subscribe(message => {
        this.messages.push(message);
      }),
      this.socketService.onProductShared().subscribe(product => {
        this.messages.push({ type: 'product', data: product });
      }),
      this.socketService.onError().subscribe(error => {
        console.error('Socket error:', error);
        // Handle error (e.g., show toast notification)
      })
    );
  }

  ngOnDestroy() {
    this.subscriptions.forEach(sub => sub.unsubscribe());
    this.socketService.disconnect();
  }

  joinRoom(roomId: string) {
    if (this.currentRoom) {
      this.socketService.leaveRoom(this.currentRoom);
    }
    this.socketService.joinRoom(roomId);
    this.currentRoom = roomId;
    this.messages = []; // Clear messages when joining a new room
    // Fetch previous messages for this room
    this.fetchPreviousMessages(roomId);
  }

  sendMessage() {
    if (this.currentRoom && this.currentMessage.trim()) {
      this.socketService.sendMessage(this.currentRoom, this.currentMessage);
      this.currentMessage = '';
    }
  }

  shareProduct(productId: number) {
    if (this.currentRoom) {
      this.socketService.shareProduct(this.currentRoom, productId);
    }
  }

  private fetchPreviousMessages(roomId: string) {
    // Implement API call to fetch previous messages
    // Update this.messages with the fetched messages
  }
}
```

## Chat Component Template

Create the template for the chat component:

```html
<!-- src/app/components/chat/chat.component.html -->
<div class="chat-container">
  <div class="chat-messages">
    <div *ngFor="let message of messages" class="message" [ngClass]="{'own-message': message.user === currentUserId}">
      <ng-container *ngIf="message.type !== 'product'; else productTemplate">
        <strong>{{ message.user }}:</strong> {{ message.msg }}
      </ng-container>
      <ng-template #productTemplate>
        <div class="shared-product">
          <img [src]="message.data.product.image_url" alt="Product Image">
          <h4>{{ message.data.product.name }}</h4>
          <p>Price: {{ message.data.product.price | currency }}</p>
          <p>{{ message.data.product.description }}</p>
        </div>
      </ng-template>
    </div>
  </div>
  <div class="chat-input">
    <input [(ngModel)]="currentMessage" (keyup.enter)="sendMessage()" placeholder="Type a message...">
    <button (click)="sendMessage()">Send</button>
  </div>
</div>
```

## Using the Chat Component

To use the chat component in your application:

1. Add the ChatComponent to your module declarations.
2. Use the component in your template:

```html
<app-chat></app-chat>
```

3. Make sure to handle room joining, either by passing the room ID to the component or handling it within the component based on your application's logic.

## Creating Chat Rooms

To create a new chat room, you'll need to make an API call. Here's an example