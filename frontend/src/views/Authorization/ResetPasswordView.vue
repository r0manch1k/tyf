<template>
	<svg
		xmlns="http://www.w3.org/2000/svg"
		style="display: none"
		width="16"
		height="16"
		fill="currentColor"
		class="bi bi-arrow-left-short"
		viewBox="0 0 16 16"
	>
		<symbol id="arrow-left" fill="currentColor" viewBox="0 0 16 16">
			<path
				fill-rule="evenodd"
				d="M12 8a.5.5 0 0 1-.5.5H5.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5H11.5a.5.5 0 0 1 .5.5"
			/>
		</symbol>
	</svg>
	<div class="container-fluid">
		<div
			class="flex row vh-100 align-items-center justify-content-center"
			style="min-height: 100vh"
		>
			<div class="col-12 row col-sm-8 col-md-6 col-lg-5 col-xl-4">
				<!-- TODO: ADD MESSAGES -->
				<div
					class="bg-secondary rounded p-4"
					style="border-radius: 1rem !important"
				>
					<div class="py-3 mb-4">
						<div class="position-relative">
							<div class="position-absolute top-50 start-0 translate-middle-y">
								<router-link to="/login">
									<a class="float-start">
										<svg width="35" height="35" role="img">
											<use xlink:href="#arrow-left" />
										</svg>
									</a>
								</router-link>
							</div>
							<div
								id="reset-password-title"
								class="position-absolute top-50 start-50 translate-middle"
								style="width: 60% !important"
							>
								<h3 class="text-center fs-5" style="margin: 0 !important">
									Восстановление пароля
								</h3>
							</div>
						</div>
					</div>
					<form method="post" role="form">
						<div class="form-floating mb-3">
							<EmailField />
						</div>
						<button
							type="submit"
							class="btn btn-primary py-3 w-100 mb-4"
							style="border-radius: 1rem !important"
						>
							<label style="color: var(--dark) !important">Продолжить</label>
						</button>
					</form>
					<router-link to="/register">
						<p class="text-center mb-0">
							<a>Создать новый аккаунт</a>
						</p>
					</router-link>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import EmailField from '@/components/Authorization/Fields/EmailField.vue'
</script>

<style scoped></style>
